from flask import render_template, request, url_for, redirect
from app_abraam import bp
from extensions import db
from models.voorwerpen import Voorwerpen

@bp.route('/')
def index():
    return render_template('index.html')

#https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# We used this link for "overzicht", "toevoegen"
@bp.route('/toevoegen/', methods=('GET', 'POST'))
def toevoegen():
    voorwerpen = Voorwerpen.query.all()

    if request.method == 'POST':
        # Create a new Voorwerpen object with the form data
        nieuwe_voorwerp = Voorwerpen(voorwerp_naam=request.form['voorwerp_naam'], hoeveelheid=request.form['hoeveelheid'])
        # Add the new object to the session and commit the changes
        db.session.add(nieuwe_voorwerp)
        db.session.commit()

    return render_template('materialen/toevoegen.html')

@bp.route('/overzicht/', methods=('GET', 'POST'))
def overzicht():
    if request.method == 'POST':
        search_query = request.form['search']
        # Query Voorwerpen objects matching the search query
        voorwerpen = Voorwerpen.query.filter(Voorwerpen.voorwerp_naam.like('%{}%'.format(search_query))).all()
    else:
        # Query all Voorwerpen objects
        voorwerpen = Voorwerpen.query.all()

    return render_template('materialen/overzicht.html', voorwerpen=voorwerpen)

#https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application#step-6-editing-a-record 
#we used this link for "bewerken", "verwijderen"
@bp.route('/bewerken/<int:voorwerp_id>', methods=('GET', 'POST'))
def bewerken(voorwerp_id):
    voorwerp = Voorwerpen.query.get_or_404(voorwerp_id)

    if request.method == 'POST':
        # Update the existing Voorwerpen object with the form data
        voorwerp.voorwerp_naam = request.form['voorwerp_naam']
        voorwerp.hoeveelheid = request.form['hoeveelheid']
        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('abraam.overzicht'))

    return render_template('bewerken/bewerken.html', voorwerp=voorwerp)

@bp.route('/verwijderen/<int:voorwerp_id>', methods=['GET', 'POST'])
def verwijderen(voorwerp_id):
    voorwerp = Voorwerpen.query.get_or_404(voorwerp_id)
    
    # Delete the Voorwerpen object from the session and commit the changes
    db.session.delete(voorwerp)
    db.session.commit()
    
    return redirect(url_for('abraam.overzicht'))
