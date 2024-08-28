from flask import Flask, request, send_file, jsonify, render_template, url_for, session, redirect
from flask_session import Session  
from speech_to_text import save_text_to_audio
import os
import threading
import wave
import pyaudio
import whisper
import azure.cognitiveservices.speech as speechsdk
import openai
import requests
import cv2
import time
from flask_cors import CORS
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key =b'\xf3tGg\xe3\x08\xe8\xae\xdd\x8fI"p\xd5\xdc\xe1\x8e\xf7\x05\xe9\xd8^\xfe\x17'
app.config["SESSION_TYPE"] = "filesystem"  # Sla sessies op het bestandssysteem op voor eenvoud
Session(app)

# Pad en extensies configureren
UPLOAD_WAV = './uploads'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_WAV'] = UPLOAD_WAV
os.makedirs(UPLOAD_WAV, exist_ok=True)

# Azure en Whisper configuraties
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = "azure"
openai.api_version = "2023-09-01-preview"

endpoint = "https://visionresource-schoonmaak.cognitiveservices.azure.com/"
subscription_key = "046c89a677bf485ea3a34a020d82f6e5"
analyze_url = endpoint + "vision/v3.2/analyze"

speech_model_name = "whisper"
speech_deployment_id = "whisper" #This will correspond to the custom name you chose for your deployment when you deployed a model."
audio_language="nl"

# Dummy gebruikersdata, in een echte applicatie zou je een database gebruiken
users = {"admin": "password123"}

@app.route('/')
def index():
    return render_template('inlog.html')

@app.route('/form_inlog', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name1 = request.form['gebruikersnaam']
        pwd = request.form['wachtwoord']
        if name1 not in users:
            return render_template('inlog.html', info='Onbekende gebruiker')
        elif users[name1] != pwd:
            return render_template('inlog.html', info='Onjuiste wachtwoord')
        else:
            session.clear()  # Reset de sessie
            return render_template('index.html')  # Veronderstelt dat er een 'home'-route is voor ingelogde gebruikers

@app.route('/registratie', methods=['GET', 'POST'])
def registratie():
    global users  # Voeg deze regel toe om aan te geven dat je de globale 'users' wilt aanpassen
    if request.method == 'POST':
        username = request.form['gebruikersnaam']
        password = request.form['wachtwoord']
        # Controleer of de gebruikersnaam al bestaat
        if username in users:
            return render_template('registratie.html', info='Gebruikersnaam bestaat al')
        else:
            # Voeg de nieuwe gebruiker toe aan de gebruikersdatabase
            users[username] = password  # Zorg dat je de gebruiker toevoegt aan de 'users'-dict
            return render_template('login.html')  # Stuur de gebruiker door naar de inlogpagina na registratie


# PyAudio initialiseren
p = pyaudio.PyAudio()
stream = None
frames = []

def start_recording():
    global stream, frames
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while stream.is_active():
        data = stream.read(CHUNK)
        frames.append(data)

# Functies
@app.route('/start', methods=['POST'])
def start():
    global stream
    if stream is None or not stream.is_active():
        threading.Thread(target=start_recording).start()
        return jsonify({"status": "recording started"})
    else:
        return jsonify({"status": "recording is already active"})

@app.route('/stop', methods=['POST'])
def stop():
    global stream, frames
    if stream is not None and stream.is_active():
        stream.stop_stream()
        stream.close()
        # Sla de opgenomen audio op
        WAVE_OUTPUT_FILENAME = 'output.wav'
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Zet audio om naar tekst
        input_text = audio_to_text(WAVE_OUTPUT_FILENAME)

        # Krijg AI respons
        response_text = analyze_audio(input_text)

        # Zet AI tekst om naar audio
        RESPONSE_AUDIO_FILENAME = "speech.wav"
        text_to_audio(response_text, RESPONSE_AUDIO_FILENAME)

        stream = None  # Reset de stream
        return send_file(RESPONSE_AUDIO_FILENAME, as_attachment=True)
    else:
        return jsonify({"status": "recording is not active"})

@app.route('/message', methods=['POST'])
def message():
    data = request.json  # Verwacht dat het bericht in JSON-formaat is
    incoming_message = data.get('message', '')  # Haal de 'message' sleutel op uit de JSON
    print(f"Received message: {incoming_message}")  # Log het bericht, of sla het op in een database

    # Call the analyze_audio function to get AI response
    response_message = analyze_audio(incoming_message)

    # Stuur een responsbericht terug
    return jsonify({"status": "success", "response": response_message})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def audio_to_text(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename, fp16=False)
    return result["text"]

def text_to_audio(text, model="tts-1", voice="alloy"):
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = "tts"  # Replace with your deployment name
    
    api_endpoint = f"{endpoint}/openai/deployments/{deployment_name}/audio/speech?api-version=2024-02-15-preview"

    # Request headers
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    # Request body
    data = {
        "model": model,
        "input": text,
        "voice": voice
    }

    # Make POST request to Azure OpenAI Service
    response = requests.post(api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        # Assuming the response contains the audio file
        target_directory = 'webapp'  # Naam van de doelmap
        target_file_path = os.path.join(target_directory, 'speech.wav')  # Volledige pad naar het bestand

        os.makedirs(target_directory, exist_ok=True)

        with open(target_file_path, "wb") as f:
            f.write(response.content)
        print(f"Speech saved as {target_file_path}")
        return target_file_path
    else:
        print("Failed to generate speech:", response.text)
        return response




def analyze_audio(text):
    # Haal de huidige conversatiecontext op uit de sessie, of initialiseer deze als leeg als deze nog niet bestaat
    if 'conversation' not in session:
        session['conversation'] = []
    
    # Voeg de nieuwe gebruikerstekst toe aan de conversatiecontext
    session['conversation'].append({"role": "user", "content": text})

    ai_prompt = {
        "role": "system",
        "content": "You are an cleaning assistant, give tips in what to do. You should not use more than 500 characters. React in the language the question is asked",
    }
    
    # Genereer een respons op basis van de volledige conversatiecontext
    response = openai.chat.completions.create(
        model="gpt35",  # Pas dit aan naar het gewenste model
        messages=[ai_prompt] + session['conversation'], 
        max_tokens=400,
    )
    # Voeg de AI-respons toe aan de conversatiecontext
    ai_response = response.choices[0].message.content
    session['conversation'].append({"role": "system", "content": ai_response})
    
    # Sla de bijgewerkte conversatiecontext op in de sessie
    session.modified = True
    
    return ai_response

@app.route('/camera')
def camera():
    return render_template('foto.html')

@app.route('/capture')
def capture_image():
    print("capture_image() functie is aangeroepen")  # Dit print een bericht in de server console

    images_dir = os.path.join(app.root_path, 'static', 'images')
    os.makedirs(images_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    time.sleep(2)

    success, frame = cap.read()
    if success:
        filename = "captured_image.jpg"
        file_path = os.path.join(images_dir, filename)
        cv2.imwrite(file_path, frame)  # Sla de afbeelding op

        file_url = url_for('static', filename=f'images/{filename}')
        message = f"Afbeelding succesvol opgeslagen als {filename}"
        cap.release()  # Laat de webcam los
        
# Afbeelding analyseren
    tags = analyze_image(file_path)

    if tags:
        analysis_text = "Geïdentificeerde objecten: " + ", ".join(tags)

        # Tekst omzetten naar audio
        audio_path = text_to_audio(analysis_text)
        if audio_path:
            audio_url = url_for('static', filename=os.path.basename(audio_path))

            return jsonify({
                "status": "success",
                "image_url": file_url,
                "analysis_text": analysis_text,
                "audio_url": audio_url,
                "message": message
            })
        else:
            return jsonify({"status": "error", "message": "Kon de tekst niet omzetten naar audio"})
    else:
        return jsonify({"status": "error", "message": "Kon de afbeelding niet analyseren"})
    
def analyze_image(image_path):
    # De parameters voor het type analyse die je wilt uitvoeren.
    params = {
        'visualFeatures': 'Tags'
    }
    # De headers voor de POST-request.
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }

    # Lees de afbeelding en stuur als byte stream
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)

    if response.status_code == 200:
        response_json = response.json()
        tags = [tag['name'] for tag in response_json['tags'] if tag['confidence'] > 0.5]
        return tags  # Retourneer een lijst met tags
    else:
        print("Error analyzing image:", response.status_code, response.text)
        return None  # Of je kunt hier een foutbericht of een lege lijst teruggeven, afhankelijk van je voorkeur


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})

    # Controleer het bestandstype en kies de juiste verwerkingsmethode
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    if file_ext in {'jpg', 'jpeg', 'png'}:
        # Verwerk afbeeldingsbestanden
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Analyseer de afbeelding (implementeer deze functie op basis van je vereisten)
            tags = analyze_image(filepath)

            return jsonify({"status": "success", "tags": tags})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    elif file_ext in {'wav'}:
        # Verwerk audiobestanden
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_WAV'], filename)
            file.save(filepath)

            input_text = audio_to_text(filepath)
            response_text = analyze_audio(input_text)
            save_text_to_audio(response_text)

            return send_file("speech.wav", as_attachment=True)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    else:
        return jsonify({"status": "error", "message": "Unsupported file type"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)