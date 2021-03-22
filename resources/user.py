from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                get_jwt, get_jwt_identity)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

# from main import BLACKLIST
from blacklist import BLACKLIST
from models.user import UserModel


class Users(Resource):
    def get(self):
        users = UserModel.find_all()
        return {'users': [user.json() for user in users]}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='username required')
    parser.add_argument('password', type=str, required=True, help='password required')

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
