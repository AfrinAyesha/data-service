from flask import Flask
from flask_restful import Api
from flask_jwt_extended import jwt_manager

from resources.agent import AgentsList, AgentRegister
from resources.user import Users
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'data_service_key'

api = Api(app)
# jwt = jwt_manager(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Users, '/users')
api.add_resource(AgentRegister, '/register/agent')
api.add_resource(AgentsList, '/agents')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
