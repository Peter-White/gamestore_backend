from app import app, db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    descriptionURL = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    imageURL = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(2))
    type = db.Column(db.String(20), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer)
