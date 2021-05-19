from flask_restplus import fields
from api_rest.api.restplus import api

game_post = api.model('Game post single model', {
    'game_id': fields.String(readOnly=True, description='The unique identifier of a game post')
})
piece = api.model('A dominoes piece', {
    'first': fields.Integer(readOnly=True, description='First value in dominoes piece'),
    'second': fields.Integer(readOnly=True, description='Second value in dominoes piece')
})
game_full = api.model('Game post full model', {
    'game_id': fields.String(readOnly=True, description='The unique identifier of a game post'),
    'owner_id': fields.String(required=True, description='User identifier', attribute="owner"),
    'pub_date': fields.DateTime,
    'enabled': fields.Boolean(attribute="status"),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_games = api.inherit('Page of Game posts', pagination, {
    'items': fields.List(fields.Nested(game_full))
})

user = api.model('User', {
    'identifier': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='User name'),
    'nickname': fields.String(required=False, description='nickname name'),
    'password': fields.String(required=True, description='User password'),
    'role': fields.String(required=False, description='User role'),
    'enabled': fields.Boolean(required=False, description='status password', default=True),
})
login = api.model('Login', {
    'name': fields.String(required=True, description='User nickname or identifier'),
    'password': fields.String(required=True, description='User password'),
})
# user_post = api.model('User', {
#     'identifier': fields.String(readOnly=True, description='The unique identifier'),
#     'name': fields.String(required=True, description='User name'),
#     'nickname': fields.String(required=False, description='nickname name'),
#     'password': fields.String(required=True, description='User password'),
# })

user_light = api.model('User', {
    'identifier': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='User name'),
    'nickname': fields.String(required=False, description='nickname name'),
})

user_with_games = api.inherit('User with games', user, {
    'games': fields.List(fields.Nested(game_post))
})

games_users = api.inherit('Game users', game_post, {
    'users': fields.List(fields.Nested(user_light))
})
