from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from models.user import UserModel
from resources.agent import AgentsList, AgentRegister, Agent
from resources.policy import Policy
from resources.user import Users, UserLogin, UserLogout, TokenRefresh
from resources.customer import CustomerList, Customer, CustomerRegister
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)
app.secret_key = 'data_service_key'
CORS(app)

api = Api(app)


@app.before_first_request
def create_tables():
    print('creating')
    db.create_all()


jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    return {'userType': user.usertype}


@jwt.expired_token_loader
def expired_token_callback(header, data):
    return {
        'message': 'The token has expired.',
        'error': 'token_expired'
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }, 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return {
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }, 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return {
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }, 401


api.add_resource(Users, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(AgentRegister, '/register/agent')
api.add_resource(AgentsList, '/agents')
api.add_resource(Agent, '/agent')
api.add_resource(CustomerRegister, '/register/customer')
api.add_resource(CustomerList, '/customers')
api.add_resource(Customer, '/customer/<int:customer_id>')
api.add_resource(Policy, '/policy')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
