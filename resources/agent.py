from flask_restful import Resource, reqparse

from models.agent import AgentModel
from models.user import UserModel


class AgentsList(Resource):
    def get(self):
        agents = AgentModel.find_all()
        return {
            'agents': [agent.json() for agent in agents]
        }, 200


class AgentRegister(Resource):
    user_reg_parser = reqparse.RequestParser()
    user_reg_parser.add_argument('fullname', type=str, required=True, help='full name required')
    user_reg_parser.add_argument('username', type=str,required=True, help='username required')
    user_reg_parser.add_argument('email', type=str, required=True, help='emailId required')
    user_reg_parser.add_argument('password', type=str, required=True, help='password required')
    user_reg_parser.add_argument('commision_percentage', type=int, required=True, help='commision percentage required')

    def post(self):
        data = AgentRegister.user_reg_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'username already exists'}, 400
        user = UserModel(data['username'], data['password'], usertype='agent')
        user.save_to_db()
        print('user', user.id)
        agent = AgentModel(user.id, data['fullname'], data['email'], data['commision_percentage'])
        agent.save_to_db()
        return {'message': 'user created successfully'}, 201

