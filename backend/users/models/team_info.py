from . import db


class TeamInfo(db.Model):
    __tablename__ = "team_info"
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    plan = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "plan": self.plan,
        }

    def __repr__(self):
        return f"{self.uuid} <{self.username}>"
