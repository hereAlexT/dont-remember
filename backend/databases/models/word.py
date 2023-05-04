import datetime
from . import db

class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.String(80), primary_key=True)
    dict_id = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    last_review = db.Column(db.Boolean, nullable=False, default=False)
    next_review = db.Column(db.DateTime, nullable=True)

    # This is a helper method to convert the model to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'dict_id': self.dict_id,
            'user_id': self.user_id,
            'last_review': self.last_review.isoformat() if self.last_review else None,
            'next_review': self.next_review.isoformat() if self.next_review else None,
        }

    def __repr__(self):
        return f'<Word {self.id}>'