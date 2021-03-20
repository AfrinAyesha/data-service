from db import db


class CustomerModel(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    name = db.Column(db.String(80))
    dob = db.Column(db.Date)
    email = db.Column(db.String(80))
    address = db.Column(db.String(80))
    contact_num = db.Column(db.Integer)
    alternate_num = db.Column(db.Integer)
    policies = db.relationship('PolicyModel', backref='customer')

    # def __init__(self, customer_id, name, dob, email, address, contact_num, alternate_num):
    #     self.customer_id = customer_id
    #     # self.agent_id = agent_id
    #     self.name = name
    #     self.dob = dob
    #     self.email = email
    #     self.address = address,
    #     self.contact_num = contact_num
    #     self.alternate_num = alternate_num

    def json(self):
        return {
            'agent_id': self.agent_id,
            'customer_id': self.id,
            'name': self.name,
            'dob': str(self.dob),
            'email': self.email,
            'address': self.address,
            'contact_num': self.contact_num,
            'alternate_num': self.alternate_num,
            'policies': [policy.json() for policy in self.policies]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_agent_id(cls, agent_id):
        return cls.query.filter_by(agent_id=agent_id)

    @classmethod
    def find_by_customer_id(cls, customer_id):
        return cls.query.filter_by(customer_id=customer_id).first_or_404(
            description='No customer found for {}'.format(customer_id))

    @classmethod
    def find_all(cls):
        return cls.query.all()
