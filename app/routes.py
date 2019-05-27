from app import app, db
from flask import request, jsonify
from app.models import Game, Cart

# set index route to return nothing, just so no error
@app.route('/')
def index():
    return ''

@app.route('/api/games', methods=['GET'])
def getAllGames():
    try:

        data = []

        for game in Game.query.all():
            gameJSON = {}
            gameJSON["id"] = game.id
            gameJSON["title"] = game.title
            gameJSON["descriptionURL"] = game.descriptionURL
            gameJSON["price"] = game.price
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
        args = request.args

        id = args.get("id")
        title = args.get('title')

        gameJSON = {}

        if id and not title:
            game = Game.query.filter_by(id = id).first()
        elif not id and title:
            game = Game.query.filter_by(title = title).first()
        else:
            return jsonify({ "error#420": "Invalid params" })

        gameJSON["id"] = game.id
        gameJSON["title"] = game.title
        gameJSON["descriptionURL"] = game.descriptionURL
        gameJSON["price"] = game.price
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
        price = request.headers.get("price")
        type = request.headers.get("type")
        genre = request.headers.get("genre")
        quantity = request.headers.get("quantity")

        game = Game(title = title, descriptionURL = descriptionURL, imageURL = imageURL, rating = rating, price = price, type = type, genre = genre, quantity = quantity)

        db.session.add(game)
        db.session.commit()

        return jsonify({ "Success": f'{title} added' })

    except:
        return jsonify({"error#1337": "Game could not be saved"})

@app.route('/api/game/update/<id>', methods=['GET', 'PATCH'])
def updateGame(id=-1):
    try:
        title = request.headers.get("title")
        descriptionURL = request.headers.get("descriptionURL")
        imageURL = request.headers.get("imageURL")
        price = request.headers.get("price")
        rating = request.headers.get("rating")
        type = request.headers.get("type")
        genre = request.headers.get("genre")
        quantity = request.headers.get("quantity")

        data = {}
        if title:
            data["title"] = title
        if descriptionURL:
            data["descriptionURL"] = descriptionURL
        if imageURL:
            data["imageURL"] = imageURL
        if price:
            data["price"] = price
        if rating:
            data["rating"] = rating
        if type:
            data["type"] = type
        if genre:
            data["genre"] = genre
        if quantity:
            data["quantity"] = quantity

        Game.query.filter_by(id = id).update(data)
        db.session.commit()

        return jsonify({ "Success" : "game updated" })

    except:
        return jsonify({ "error#80085": "Failed To Update" })

@app.route('/api/game/delete/<id>', methods=['GET', 'DELETE'])
def deleteGame(id=-1):
    try:
        game = Game.query.filter_by(id=id).first()

        cart = Cart.query.filter_by(game_id = id).all()

        if cart:
            for game in cart:
                db.session.delete(game)
                db.session.commit()

        db.session.delete(game);
        db.session.commit();

        return jsonify({ "Success" : "game killed" })
    except:
        return jsonify({ "error#010101010101": "Failed To Delete" })


@app.route('/api/cart', methods=['GET'])
def getCart():
    try:
        data = []

        for item in Cart.query.all():
            cartJSON = {}
            cartJSON["id"] = item.id
            cartJSON["game_id"] = item.game_id
            cartJSON["quantity"] = item.quantity
            data.append(cartJSON)

        return jsonify(data)

    except:
        return jsonify({ 'error#7734': "Failed to get cart" })

@app.route('/api/cart/save', methods=['GET', 'POST'])
def addToCart(game_id=-1):
    try:
        game_id = request.headers.get("game_id")

        cart = Cart(game_id = game_id, quantity = 1)
        db.session.add(cart)
        db.session.commit()

        return jsonify({ "Success" : "Game added to cart" })
    except:
        return jsonify({ 'error#101101101101': "Failed to get cart" })

@app.route('/api/cart/remove', methods=['GET', 'DELETE'])
def removeFromCart():
    try:
        id = request.headers.get("id")

        item = Cart.query.filter_by(id=id).first()

        db.session.delete(item)
        db.session.commit()

        return jsonify({ "Success" : "game expelled from cart" })
    except:
        return jsonify({ 'error#101101101101': "Failed to delete from cart" })

@app.route('/api/cart/checkout', methods=['GET', 'DELETE'])
def checkoutGameFromCart(id=-1):
    try:
        id = request.headers.get("id")

        cartItem = Cart.query.filter_by(id=id).first()
        game = Game.query.filter_by(id=cartItem.game_id).first()

        if game.quantity:
            newQuant = game.quantity - cartItem.quantity

            Game.query.filter_by(id = game.id).update({ "quantity": newQuant })

        db.session.delete(cartItem)
        db.session.commit()

        return jsonify({ "Success" : "game expelled from cart" })
    except:
        return jsonify({ 'error#101101101101': "Failed to delete from cart" })

@app.route('/api/cart/quantity/<id>', methods=["GET", "PATCH"])
def updateGameQuantity(id=-1):
    try:
        method = request.headers.get("method")
        cartItem = Cart.query.filter_by(id = id).first()

        if method == "More":
            Cart.query.filter_by(id = id).update({ "quantity": cartItem.quantity + 1 })
        else:
            Cart.query.filter_by(id = id).update({ "quantity": cartItem.quantity - 1 })

        db.session.commit()

        return jsonify({ "Success" : "cart game update" })
    except:
        return jsonify({ 'error#0000000000000001': 'cart game failed to update' })

@app.route('/api/cart/game/<id>', methods=["GET"])
def getCartGame(id=-1):
    try:
        cartItem = {}

        query = Cart.query.filter_by(id = id).first()

        if query:
            cartItem["id"] = query.id
            cartItem["game_id"] = query.game_id
            cartItem["quantity"] = query.quantity

        return jsonify(cartItem)
    except:
        return jsonify({ 'error#12357913': 'cart game not found' })
