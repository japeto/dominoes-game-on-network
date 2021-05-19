import uuid
import hashlib
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def reset_database():
    from api_rest.database.models import DGame, DUser, DRole
    db.drop_all()
    db.create_all()

    db.session.add(DRole("admin"))
    db.session.add(DRole("user"))
    pswd = hashlib.md5("Dominoes#2".encode())
    admin_id = "00000000"

    db.session.add(DUser(admin_id, "ADMINISTRADOR", pswd.hexdigest(), role = "admin", enabled = True))
    game_id = str(uuid.uuid1())[:6]
    db.session.add(DGame(game_id, admin_id))
    db.session.commit()

