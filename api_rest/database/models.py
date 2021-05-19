# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime

from api_rest.database import db, reset_database

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name



class DRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    read = db.Column(db.Integer)
    write = db.Column(db.Integer)
    delete = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.read = 1
        self.write = 1
        self.delete = 0

    def __repr__(self):
        return '<DRole {self.name} [{self.read, self.write, self.delete}]>'

class DUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(50))
    name = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    password  = db.Column(db.String(50))
    role  = db.Column(db.Integer)
    enabled = db.Column(db.Boolean)

    def __init__(self, identifier, name, password, role = "user", enabled = True, nickname=""):
        self.identifier = identifier
        self.name = name
        self.nickname = nickname
        self.password = password
        self.role = DRole.query.filter(DRole.name == role).one()
        self.role = self.role.id if self.role else 0
        self.enabled = enabled

    def __repr__(self):
        return "<DUser {self.name} {self.role}>"

class DGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(50))
    owner = db.Column(db.String(50))
    winner = db.Column(db.String(50))
    status  = db.Column(db.String(50))
    pub_date = db.Column(db.DateTime)

    def __init__(self, game_id, owner, winner=None, pub_date = None, status="Open"):
        self.game_id = game_id
        self.owner = owner
        self.winner = winner
        self.status = status
        if pub_date is None:
            self.pub_date = datetime.utcnow()

    def __repr__(self):
        return '<Game {self.game_id, self.owner, self.winner, self.status}>'