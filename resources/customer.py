from datetime import datetime

from flask_restful import Resource, reqparse

from models.user import UserModel
from models.agent import AgentModel
from models.customer import CustomerModel


class CustomerList(Resource):
    def get(self):
        customers = CustomerModel.find_all()
        return {'customers': [customer.json() for customer in customers]}, 200


class Customer(Resource):
    def get(self, customer_id):
        customer = CustomerModel.find_by_customer_id(customer_id)
        return {'customer': customer.json()}


class CustomerRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username required')
    parser.add_argument('password', type=str, required=True, help='password required')
    parser.add_argument('agent_id', type=str, required=True, help='agent Id required')
    parser.add_argument('name', type=str, required=True, help='name required')
    parser.add_argument('email', type=str, required=True, help='email required')
    parser.add_argument('dob', type=str, required=True,
                        help='dob required')
    parser.add_argument('address', type=str, required=True,
                        help='address required')
    parser.add_argument('contact_num', type=str, required=True, help='contact number required')
    parser.add_argument('alternate_num', type=str, required=True, help='alternate number required')

    def post(self):
        data = CustomerRegister.parser.parse_args()
        print('data', data['address'])
        if UserModel.find_by_username(data['username']):
            return {'message': 'username already exists'}, 400
        if AgentModel.find_by_agent_id(data['agent_id']) is None:
            return {'message': 'Invalid agent Id'}, 400
        user = UserModel(data['username'], data['password'], usertype='customer')
        user.save_to_db()
        agent = AgentModel.find_by_agent_id(data['agent_id'])
        d, m, y = data['dob'].split('-')
        converted_dob = datetime(int(y), int(m), int(d))
        customer = CustomerModel(customer_id=user.id, agent=agent, name=data['name'], dob=converted_dob,
                                 email=data['email'],
                                 address=data['address'], contact_num=data['contact_num'],
                                 alternate_num=data['alternate_num'])
        print('got it', customer.json())
        customer.save_to_db()
        return {'message': 'customer Registered Successfully'}, 201
