from . import db


class User(db.Model):
    __tablename__ = "users"
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    token_expiration = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "username": self.username,
            "password": self.password,
        }

    def __repr__(self):
        return f"{self.uuid} <{self.username}>"
