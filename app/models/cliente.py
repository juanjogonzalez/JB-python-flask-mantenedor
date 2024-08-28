from app.extensions import db

class Cliente(db.Model):

    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    active = db.Column(db.Boolean, nullable=False)