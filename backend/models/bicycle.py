from datetime import datetime
from backend.extensions import db

class Bicycle(db.Model):
    __tablename__ = 'bicycle'

    bicycle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bicycle_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    type = db.Column(db.String(30), nullable=False, default='City')
    status = db.Column(db.String(20), nullable=False, default='Available', index=True)
    rental_rate = db.Column(db.Numeric(10, 2), nullable=False, default=5.00)
    owner_id = db.Column(db.Integer, db.ForeignKey('rental_owner.owner_id', ondelete='CASCADE'), nullable=False, index=True)
    station_id = db.Column(db.Integer, db.ForeignKey('station.station_id', ondelete='SET NULL'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    rentals = db.relationship('Rental', backref='bicycle', lazy=True)

    def to_dict(self):
        return {
            'bicycle_id': self.bicycle_id,
            'bicycle_number': self.bicycle_number,
            'type': self.type,
            'status': self.status,
            'rental_rate': float(self.rental_rate) if self.rental_rate is not None else 0.0,
            'owner_id': self.owner_id,
            'station_id': self.station_id,
            'station_name': self.station.station_name if self.station else None,
            'station_location': self.station.location if self.station else None,
            'owner_name': self.owner.name if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

