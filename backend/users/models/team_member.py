from . import db


class TeamMember(db.Model):
    __tablename__ = "team_member"
    uuid = db.Column(db.Integer, primary_key=True)
    team_uuid = db.Column(db.Integer, db.ForeignKey("team_info.uuid"), nullable=False)
    user_uuid = db.Column(db.Integer, db.ForeignKey("users.uuid"), nullable=False)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "plan": self.plan,
        }

    def __repr__(self):
        return f"{self.uuid} <{self.username}>"
