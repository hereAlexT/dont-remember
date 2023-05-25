from . import db


class WordList(db.Model):
    __tablename__ = "word_list"
    uuid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    user_uuid = db.Column(db.Integer, nullable=False)
    last_review_time = db.Column(db.DateTime, nullable=False)
    next_review_time = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "word": self.word,
            "user_uuid": self.user_uuid,
            "last_review_time": self.last_review_time,
            "next_review_time": self.next_review_time,
        }

    def __repr__(self):
        return f"{self.uuid} <{self.word}>"
