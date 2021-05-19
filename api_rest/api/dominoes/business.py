import uuid
import hashlib
from flask import abort, jsonify
from api_rest.database import db, reset_database
from api_rest.database.models import DGame, DUser

def create_game(data):
    game_id = data["game_id"] if data["game_id"] else str(uuid.uuid1())[:6]
    a_game = DGame.query.filter(DGame.game_id == game_id).first()
    if a_game:
        abort(409, description="game_id already exists")
    owner_id = data.get('owner_id')
    pub_date = data.get('pub_date')
    pub_date = pub_date if  pub_date else None
    a_game = DGame(game_id, owner_id, winner=None, pub_date = pub_date)
    db.session.add(a_game)
    db.session.commit()
    return game_id

def update_game(game_id, data):
    a_game = DGame.query.filter(DGame.game_id == game_id).one()
    a_game.status = data.get('status')
    a_game.winner = data.get('winner')
    db.session.add(a_game)
    db.session.commit()

def delete_game(game_id, user_id):
    a_game = DGame.query.filter(DGame.game_id == game_id, DGame.owner==user_id).one()
    a_game.status = "Close"
    db.session.add(a_game)
    db.session.commit()

def create_user(data):
    name = data.get('name').upper()
    identifier = data.get('identifier')
    password = data.get('password')
    pswd = hashlib.md5(password.encode())
    user = DUser(identifier, name, pswd.hexdigest(), role = "user", enabled = True, nickname="")
    db.session.add(user)
    db.session.commit()

def update_user(identifier, data):
    user = DUser.query.filter(DUser.identifier == identifier).one()
    user.name = data.get('name')
    user.nickname = data.get('nickname')
    db.session.add(user)
    db.session.commit()

def delete_user(identifier):
    user = DUser.query.filter(DUser.identifier == identifier).one()
    user.enabled = False
    db.session.add(user)
    db.session.commit()
