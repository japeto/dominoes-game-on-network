import logging
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)


from flask_restplus import Resource
from api_rest.api.dominoes.business import create_game, update_game, delete_game
from api_rest.api.dominoes.parsers import header_parser
from api_rest.api.dominoes.serializers import game_post, page_of_games, piece
from api_rest.api.dominoes.parsers import pagination_arguments
from api_rest.api.restplus import api
from api_rest.database.models import DGame
from api_rest.dominoes import *
log = logging.getLogger(__name__)

ns = api.namespace('dominoes',
                   description='Operations related to game')

_GAMES = {}

@ns.route('/game')
# @api.doc(parser=header_parser)
class GameCollection(Resource):

    @api.expect(header_parser, pagination_arguments)
    @api.marshal_with(page_of_games)
    @jwt_required
    def get(self):
        """
        Returns dominoes list.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        a_game = DGame.query
        a_game = a_game.paginate(page, per_page, error_out=False)
        return a_game

    @api.response(201, 'Game successfully created.')
    @api.response(409, 'Game id already exists.')
    @api.expect(header_parser, game_post)
    @jwt_required
    def post(self):
        """
        Creates a new dominoes game.
        """
        data=request.json
        a_game = Game.new(starting_domino=Domino(6, 6))
        user = get_jwt_identity()
        data["owner_id"] = user["identifier"]
        game_id = create_game(data)
        player_index = 0
        _GAMES[game_id]={"a_game":a_game, "player_ids":[user["identifier"],None,None,None]}
        return {"game_id":game_id,
                "game":{
                    "board": str(a_game.board),
                    "dominoes": a_game.hands[0].to_list(),
                    "turn": a_game.turn,
                    "start": a_game.starting_player,
                    "player": player_index
                }}, 201

@ns.route('/game/<string:game_id>')
@api.response(404, 'Post not found.')
class GameItem(Resource):

    @api.response(201, 'Game successfully created.')
    @api.response(404, 'Game not found.')
    @api.expect(header_parser)
    @jwt_required
    def get(self, game_id):
        """
        Get dominoes game updates
        """
        user = get_jwt_identity()
        if game_id in _GAMES and user["identifier"] in _GAMES[game_id]["player_ids"]:
            a_game = _GAMES[game_id]["a_game"]
            player_index = _GAMES[game_id]["player_ids"].index(user["identifier"])
            return {"game_id":game_id,
                "game":{
                    "board": str(a_game.board),
                    "dominoes": a_game.hands[player_index].to_list(),
                    "turn": a_game.turn,
                    "start": a_game.starting_player,
                    "player":  player_index
                }}, 200
        return None, 404

    @api.response(200, 'Game status.')
    @api.response(202, 'Game successfully updated.')
    @api.response(404, 'Game not found.')
    @api.expect(header_parser, piece)
    @jwt_required
    def put(self, game_id):
        """
        Updates a game post.
        """
        data = request.json
        user = get_jwt_identity()
        if game_id in _GAMES and user["identifier"] in _GAMES[game_id]["player_ids"]:
            a_game = _GAMES[game_id]["a_game"]
            player_index = _GAMES[game_id]["player_ids"].index(user["identifier"])
            if a_game.turn == player_index and a_game.valid_moves:
                for index, piece in enumerate(a_game.valid_moves):
                    if piece[0].first == data["first"] and piece[0].second == data["second"] and piece[1]:
                        a_game.make_move(*a_game.valid_moves[index])
                        _GAMES[game_id]["a_game"] = a_game
                        return None, 202

                    if piece[0].first == data["second"] and piece[0].second == data["first"] and not(piece[1]):
                        a_game.make_move(*a_game.valid_moves[index])
                        _GAMES[game_id]["a_game"] = a_game
                        return None, 202
            else:
                a_game.result = Result(a_game.turn, False, 100)
                _GAMES[game_id]["a_game"] = a_game
                # update_game(id, data)
                return None, 200
        return None, 404

@ns.route('/join/<string:game_id>')
@api.response(404, 'Post not found.')
class JoinGame(Resource):

    @api.response(200, 'joined to game.')
    @api.response(404, 'Game id not found or full.')
    @jwt_required
    def post(self, game_id):
        """
        Join to game.
        """
        if game_id in _GAMES and None in _GAMES[game_id]["player_ids"]:
            a_game = _GAMES[game_id]["a_game"]
            player_index = _GAMES[game_id]["player_ids"].index(None)
            user = get_jwt_identity()
            _GAMES[game_id]["player_ids"][player_index] = user["identifier"]

            return {"game_id":game_id,
                "game":{
                    "board": str(a_game.board),
                    "dominoes": a_game.hands[player_index].to_list(),
                    "turn": a_game.turn,
                    "start": a_game.starting_player,
                    "player":  player_index
                }}, 200
        return None, 404

    @api.response(204, 'Disconnected .')
    @jwt_required
    def delete(self, game_id):
        """
        Disconnected of game.
        """
        user = get_jwt_identity()
        if game_id in _GAMES and user["identifier"] in _GAMES[game_id]["player_ids"]:
            player_index = _GAMES[game_id]["player_ids"].index(user["identifier"])
            _GAMES[game_id]["player_ids"][player_index] = None
        return None, 204
