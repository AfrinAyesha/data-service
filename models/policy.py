from sqlalchemy import Sequence
from datetime import datetime

from db import db

class PolicyModel(db.Model):
    __tablename__ = 'policies'
    # policy_id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, primary_key=True)
    policy_name = db.Column(db.String(40))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    expiry_date = db.Column(db.Date)
    payment_status = db.Column(db.String(20), default=None)
    payment_due_date = db.Column(db.Date)
    due_amount = db.Column(db.Integer)
    policy_value = db.Column(db.Integer)

    # def __init__(self, policy_name, customer_id, expiry_date, payment_status, payment_due_date, due_amount, policy_value):
    #     # self.policy_id = policy_id
    #     self.policy_name = policy_name
    #     self.customer_id = customer_id
    #     self.expiry_date = expiry_date
    #     self.payment_status = payment_status,
    #     self.payment_due_date = payment_due_date,
    #     self.due_amount = due_amount,
    #     self.policy_value = policy_value

    def json(self):
        return {
            'policy_id': self.policy_id,
            'customer_id': self.customer_id,
            'policy_value': self.policy_value,
            'policy_name': self.policy_name,
            'expiry_date': str(self.expiry_date),
            'payment_status': self.payment_status,
            'due_amount': self.due_amount,
            'payment_due_date': str(self.payment_due_date),
        }



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_policy_id(cls, policy_id):
        return cls.query.filter_by(policy_id=policy_id).first_or_404(description='policy not found for {}'.format(policy_id))

    @classmethod
    def find_by_customer_id(cls, customer_id):
        return cls.query.filter_by(customer_id=customer_id)
