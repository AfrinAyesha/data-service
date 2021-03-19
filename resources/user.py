from flask_restful import Resource


from models.user import UserModel




class Users(Resource):
    def get(self):
        users = UserModel.find_all()
        return {'users': [user.json() for user in users]}, 200


