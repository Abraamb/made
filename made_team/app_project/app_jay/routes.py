from flask import render_template, url_for, request, redirect
from app_jay import bp
from extensions import db
from models.contact import contact_formulier
from flask_login import login_required, current_user



@bp.route('/contact/', methods=["GET", "POST"])
def contact():
    contact = contact_formulier.query.all()

    if request.method == 'POST':
        # Create a new Voorwerpen object with the form data
        nieuwe_contact = contact_formulier(naam=request.form['naam'], email=request.form['email'], bericht=request.form['bericht'])

        # Voeg het contact toe aan de database
        db.session.add(nieuwe_contact)
        db.session.commit()

    return render_template('contact/contact.html')
