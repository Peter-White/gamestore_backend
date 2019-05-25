from app import app, db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    descriptionURL = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    imageURL = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(2), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    quantity = db.Column(db.Integer)
