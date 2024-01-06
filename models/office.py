from app import db


class Office(db.Model):
    __tablename__ = 'Offices'

    OfficeID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Address = db.Column(db.String(255), nullable=False)
    City = db.Column(db.String(100), nullable=False)
    Country = db.Column(db.String(100), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    WorkingDays = db.Column(db.String(100), nullable=False)
    WorkingHours = db.Column(db.String(100), nullable=False)

    vehicles = db.relationship('Vehicle', backref='office', lazy=True)

    def __repr__(self):
        return f'<Office {self.Name}>'
