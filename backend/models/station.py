from datetime import datetime
from backend.extensions import db

class Station(db.Model):
    __tablename__ = 'station'

    station_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=10)
    available_bicycles = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    bicycles = db.relationship('Bicycle', backref='station', lazy=True)
    departed_rentals = db.relationship('Rental', foreign_keys='Rental.start_station_id', backref='start_station', lazy=True)
    returned_rentals = db.relationship('Rental', foreign_keys='Rental.return_station_id', backref='return_station', lazy=True)

    def to_dict(self):
        return {
            'station_id': self.station_id,
            'station_name': self.station_name,
            'location': self.location,
            'capacity': self.capacity,
            'available_bicycles': self.available_bicycles,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

