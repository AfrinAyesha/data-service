from datetime import datetime

from flask_restful import Resource, reqparse

from models.policy import PolicyModel


class Policy(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('policy_name', type=str, required=True, help='policy name required')
        parser.add_argument('customer_id', type=str, required=True, help='customer id required')
        parser.add_argument('expiry_date', type=str, required=True, help='expiry date required')
        parser.add_argument('payment_status', type=str, required=True, help='payment status required')
        parser.add_argument('payment_due_date', type=str, required=True, help='payment due date required')
        parser.add_argument('due_amount', type=str, required=True, help='due amount required')
        parser.add_argument('policy_value', type=str, required=True, help='policy value required')
        data = parser.parse_args()
        d, m, y = data['payment_due_date'].split('-')
        payment_due_date = datetime(int(y), int(m), int(d))
        dd, mm, yy = data['expiry_date'].split('-')
        print('d', d, m, y, payment_due_date)
        expiry_date = datetime(int(yy), int(mm), int(dd))
        print('dd', dd, mm, yy, expiry_date)

        policy = PolicyModel(policy_name=data['policy_name'], customer_id=data['customer_id'],
                             expiry_date=expiry_date, payment_status=data['payment_status'],
                             payment_due_date=payment_due_date, due_amount=data['due_amount'],
                             policy_value=data['policy_value'])
        policy.save_to_db()
        return {'policy': policy.json()}, 201
