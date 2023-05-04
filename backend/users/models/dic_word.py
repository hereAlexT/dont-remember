from . import db


class DicWord(db.Model):
    __tablename__ = "dic"
    uuid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    definition = db.Column(db.String, nullable=False)
    speech_part = db.Column(db.String, nullable=False)
    example = db.Column(db.String, nullable=False)
    language_A = db.Column(db.String, nullable=False)
    language_B = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "word": self.word,
            "definition": self.definition,
            "speech_part": self.speech_part,
            "example": self.example,
            "language_A": self.language_A,
            "language_B": self.language_B,
        }

    def __repr__(self):
        return f"{self.uuid} <{self.word}>"
