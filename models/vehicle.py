from app import db
# Assuming that office.py is in the same directory
from .office import Office


class Vehicle(db.Model):
    __tablename__ = 'Vehicles'

    VehicleID = db.Column(db.Integer, primary_key=True)
    Make = db.Column(db.String(50), nullable=False)
    Model = db.Column(db.String(50), nullable=False)
    Transmission = db.Column(db.String(50), nullable=False)
    Mileage = db.Column(db.Integer, nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Deposit = db.Column(db.Numeric(10, 2), nullable=False)
    OfficeID = db.Column(db.Integer, db.ForeignKey('Offices.OfficeID'), nullable=False)
    Image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Vehicle {self.Make} {self.Model}>'
