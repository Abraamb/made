from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['language'] = request.form.get('language')  # Storing the selected language in the session
        return redirect('/')
    
    language = session.get('language', 'en')  # Retrieving the stored language from the session, defaulting to 'en' (English)
    return render_template('index.html', language=language) # passing the language as a variable



if __name__ == '__main__':
    app.run(debug=True)
