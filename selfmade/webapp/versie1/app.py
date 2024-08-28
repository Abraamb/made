from flask import Flask, render_template, request, jsonify, send_file
import pyaudio
import wave
import threading
import time

app = Flask(__name__)

# Dummy gebruikersdata
users = {"admin": "password123"}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if username in users and users[username] == password:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "fail", "message": "Onjuiste gebruikersnaam of wachtwoord"}), 401

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# Globale variabelen om de opname te beheren
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

@app.route('/')
def index():
    return render_template('inlog.html')

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
        p.terminate()  # Zorg ervoor dat de PyAudio instantie netjes wordt afgesloten
        WAVE_OUTPUT_FILENAME = f'output_{int(time.time())}.wav'  # Dynamische bestandsnaam
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()
        stream = None  # Reset de stream
        return send_file(WAVE_OUTPUT_FILENAME, as_attachment=True)  # Verstuur het bestand als response
    else:
        return jsonify({"status": "recording is not active"})

@app.route('/message', methods=['POST'])
def message():
    data = request.json  # Verwacht dat het bericht in JSON-formaat is
    incoming_message = data.get('message', '')  # Haal de 'message' sleutel op uit de JSON
    print(f"Received message: {incoming_message}")  # Log het bericht, of sla het op in een database

    # Uw logica om een responsbericht te genereren
    response_message = f"Bericht ontvangen: {incoming_message}"
    
    # Stuur een responsbericht terug
    return jsonify({"status": "success", "response": response_message})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

