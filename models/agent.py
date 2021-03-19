from db import db

class AgentModel(db.Model):
    __tablename_ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(90))
    commision_percentage = db.Column(db.Integer)
    rating = db.Column(db.Integer, nullable=True)

    def __init__(self, agent_id, name, email, commision_percentage):
        self.agent_id = agent_id
        self.name = name
        self.email = email
        self.commision_percentage = commision_percentage
        self.rating = None

    def json(self):
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'email': self.email,
            'commision_percentage': self.commision_percentage,
            'rating': self.rating
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_agent_id(cls, agent_id):
        return cls.query.filter_by(agent_id=agent_id).first_or_404(description='There is no data with {}'.format(agent_id))