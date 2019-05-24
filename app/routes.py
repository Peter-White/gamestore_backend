from app import app, db
from flask import request, jsonify
from app.models import Game

# set index route to return nothing, just so no error
@app.route('/')
def index():
    return ''

@app.route('/api/games', methods=['GET', 'POST'])
def getAllGames():
    try:

        data = []

        for game in Game.query.all():
            gameJSON = {}
            gameJSON["id"] = game.id
            gameJSON["title"] = game.title
            gameJSON["descriptionURL"] = game.descriptionURL
            gameJSON["imageURL"] = game.imageURL
            gameJSON["rating"] = game.rating
            gameJSON["type"] = game.type
            gameJSON["genre"] = game.genre
            gameJSON["quantity"] = game.quantity
            data.append(gameJSON)

        return jsonify(data)

    except:
        return jsonify({ "error#302": "Failed to retrieve items" })

@app.route('/api/game', methods=['GET', 'POST'])
def getGame():
    try:
        id = request.headers.get('id')
        title = request.headers.get('title')

        gameJSON = {}
        print(id, title)

        if id and not title:
            game = Game.query.filter_by(id = id).first()
            print(game)
        elif not id and title:
            game = Game.query.filter_by(title = title).first()
        else:
            return jsonify({ "error#420": "Invalid params" })

        gameJSON["id"] = game.id
        gameJSON["title"] = game.title
        gameJSON["descriptionURL"] = game.descriptionURL
        gameJSON["imageURL"] = game.imageURL
        gameJSON["rating"] = game.rating
        gameJSON["type"] = game.type
        gameJSON["genre"] = game.genre
        gameJSON["quantity"] = game.quantity

        return jsonify(gameJSON)

    except:
        return jsonify({ "error#1337": "Something broke" })

@app.route('/api/game/save', methods=['GET', 'POST'])
def postGame():
    try:
        title = request.headers.get("title")
        descriptionURL = request.headers.get("descriptionURL")
        imageURL = request.headers.get("imageURL")
        rating = request.headers.get("rating")
        type = request.headers.get("type")
        genre = request.headers.get("genre")
        quantity = request.headers.get("quantity")

        game = Game(title = title, descriptionURL = descriptionURL, imageURL = imageURL, rating = rating, type = type, genre = genre, quantity = quantity)

        db.session.add(game)
        db.session.commit()

        return jsonify({ "Success": f'{title} added' })

    except:
        return jsonify({"error#1337": "Game could not be saved"})
