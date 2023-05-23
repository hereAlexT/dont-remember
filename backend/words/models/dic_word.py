from . import db


class DicWord(db.Model):
    __tablename__ = "dict"
    uuid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    definition = db.Column(db.String, nullable=False)
    speech_part = db.Column(db.String, nullable=False)
    example = db.Column(db.String, nullable=False)
    language_a = db.Column(db.String, nullable=False)
    language_b = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "word": self.word,
            "definition": self.definition,
            "speech_part": self.speech_part,
            "example": self.example,
            "language_A": self.language_a,
            "language_B": self.language_b,
        }

    def __repr__(self):
        return f"{self.uuid} <{self.word}>"
