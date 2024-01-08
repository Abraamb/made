from extensions import db

class Voorwerpen(db.Model):
    id_voorwerp = db.Column(db.Integer, primary_key=True)
    voorwerp_naam = db.Column(db.String(25), nullable=False)
    hoeveelheid = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Voorwerpen "{self.voorwerp_naam}">'


