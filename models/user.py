from flask_login import UserMixin
from app import db
class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Pword = db.Column(db.String(255), nullable=False)
    Country = db.Column(db.String(50))
    City = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.Email}>'
