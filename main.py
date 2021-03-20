from flask import Flask
from flask_restful import Api
from flask_jwt_extended import jwt_manager

from resources.agent import AgentsList, AgentRegister
from resources.policy import Policy
from resources.user import Users
from resources.customer import CustomerList, Customer, CustomerRegister
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'data_service_key'

api = Api(app)
# jwt = jwt_manager(app)

@app.before_first_request
def create_tables():
    print('creatingngg')
    db.create_all()


api.add_resource(Users, '/users')
api.add_resource(AgentRegister, '/register/agent')
api.add_resource(AgentsList, '/agents')
api.add_resource(CustomerRegister, '/register/customer')
api.add_resource(CustomerList, '/customers')
api.add_resource(Customer, '/customer/<int:customer_id>')
api.add_resource(Policy, '/policy')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
