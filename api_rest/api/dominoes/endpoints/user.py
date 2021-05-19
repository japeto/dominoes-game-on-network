import logging
import hashlib
import datetime
from sqlalchemy import or_, and_
from flask import Flask, request, jsonify
from flask_restplus import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)

from api_rest.api.dominoes.business import create_user, delete_user, update_user
from api_rest.api.dominoes.serializers import user, user_with_games, login
from api_rest.api.dominoes.parsers import header_parser
from api_rest.api.restplus import api
from api_rest.database.models import DUser, DGame

log = logging.getLogger(__name__)

ns = api.namespace('dominoes',
                   description='Operations related to user')

@ns.route('/user')
@ns.hide
class UserCollection(Resource):

    @api.marshal_list_with(user)
    @jwt_required
    def get(self):
        """
        Returns list of user categories.
        """
        all_user = DUser.query.all()
        return all_user

    @api.response(201, 'User successfully created.')
    @api.expect(user)
    @jwt_required
    def post(self):
        """
        Creates a new user User.
        """
        data = request.json
        create_user(data)
        return None, 201

@ns.route('/user/<string:id>')
@api.response(404, 'User not found.')
class UserItem(Resource):

    @api.marshal_with(user_with_games)
    @jwt_required
    def get(self, id):
        """
        Returns a User with a list of posts.
        """
        a_user = DUser.query.filter(DUser.identifier == id).one()
        a_user.games = DGame.query.filter(DGame.owner == id).all()
        return a_user

    @api.expect(user)
    @api.response(204, 'User successfully updated.')
    @jwt_required
    def put(self, id):
        """
        Updates a user User.

        Use this method to change the name of a user User.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "name": "New User Name"
        }
        ```

        * Specify the ID of the User to modify in the request URL path.
        """
        data = request.json
        update_user(id, data)
        return None, 204

    @api.response(204, 'User successfully deleted.')
    @jwt_required
    def delete(self, id):
        """
        Deletes user User.
        """
        delete_user(id)
        return None, 204

@ns.route('/auth/login')
@api.response(404, 'User not found.')
class Login(Resource):

    @api.response(200, 'User successfully created.')
    @api.expect(login)
    def post(self):
        """
        Authentication
        """
        req_json = request.json
        username = req_json['name']
        password = hashlib.md5(req_json['password'].encode())
        a_user = DUser.query.filter(and_(
            or_(DUser.name == username, DUser.nickname == username, DUser.identifier == username),
            # DUser.password == password.hexdigest()
        )).one()
        expires = datetime.timedelta(days=1)
        expires_refresh = datetime.timedelta(days=3)
        payload = {
            'id': a_user.id,
            'identifier': a_user.identifier,
            'username': username,
            'admin': a_user.role
        }
        token = create_access_token(identity=payload, fresh=False, expires_delta=expires)
        refresh = create_refresh_token(payload, expires_delta=expires_refresh)
        return {
            'status': 'success',
            'auth_token': token,
            'refresh_token': refresh,
        }, 200

    @api.response(201, 'Token successfully updated.')
    @jwt_refresh_token_required
    @api.expect(header_parser)
    @api.doc(security='Bearer Auth')
    def get(self):
        """
        Refresh user token
        """
        user = get_jwt_identity()
        expires_refresh = datetime.timedelta(days=3)
        new_token = create_access_token(identity=user, fresh=False)
        refresh_token = create_refresh_token(user, expires_delta=expires_refresh)

        return {
            "access_token": new_token
        }, 201
