#https://www.youtube.com/watch?v=Z1RJmh_OqeA hier wordt uitgelegd hoe je html en ccs kan koppelen met flask
from flask import Flask, request, render_template, url_for, send_file
from flask_sqlalchemy import SQLAlchemy 

# de connectie met de db https://www.youtube.com/watch?v=pPSZpCVRbvQ
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EasyForYou.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

#mijn oude connectie met de database (https://www.youtube.com/watch?v=ZQAnkjfvZAw)
#import sqlite3

# try:
#     conn = sqlite3.connect('EasyForYou.db')
#     c = conn.cursor()

#     c.execute("""CREATE TABLE upload(
#               id INTEGER NOT NULL,
#               filename VARCHAR(50),
#               data BLOB,
#               PRIMARY KEY(id)
#               )""")


#     c.close()
    
# except sqlite3.Error as error:
#     print("Error while connecting to sqlite", error)
# finally:
#     if  conn:
#         conn.close()
#         print("The SQLite connection is closed")



# deze model neemt informatie en ook data op van de file https://www.youtube.com/watch?v=pPSZpCVRbvQ
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)


# hier mee kan je kan kleine data opslaan voor de inlog pagina https://www.youtube.com/watch?v=R-hkzqjRMwM
@app.route('/')

def hello_world():
    return render_template("inlog.html")
database={'izet' : '123' ,  'abraam' : 'bekhit'}

# hier wordt de gebruikersnaam en wachtwoord gecontroleerd en dan wordt er daar op gereageerd
def index():

    return render_template("inlog.html")

@app.route('/form_inlog', methods=['POST','GET'])
def login():
    name1=request.form['gebruikersnaam']
    pwd=request.form['wachtwoord']
    if name1 not in database: 
        return render_template('inlog.html',info='Onbekende gebruiker')
    else: 
        if database[name1]!=pwd:
            return render_template('inlog.html',info='Onjuiste wachtwoord')
        else:
            return render_template('Uwdocumenten.html')  
 

# de file wordt geupload als dat gebeurd return python text https://www.youtube.com/watch?v=pPSZpCVRbvQ
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return render_template('Uwdocumenten.html')
 



if __name__ == "__main__":

    app.run(debug=True)