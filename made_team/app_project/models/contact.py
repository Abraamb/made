from extensions import db

class contact_formulier(db.Model):
    id_bericht = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    bericht = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<contact_formulier "{self.naam}">'