from datetime import datetime
from backend.extensions import db

class Rental(db.Model):
    __tablename__ = 'rental'

    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    bicycle_id = db.Column(db.Integer, db.ForeignKey('bicycle.bicycle_id', ondelete='CASCADE'), nullable=False, index=True)
    start_station_id = db.Column(db.Integer, db.ForeignKey('station.station_id', ondelete='SET NULL'), nullable=True)
    return_station_id = db.Column(db.Integer, db.ForeignKey('station.station_id', ondelete='SET NULL'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Numeric(6, 2), nullable=True)
    fare = db.Column(db.Numeric(10, 2), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Active', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    payment = db.relationship('Payment', backref='rental', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'rental_id': self.rental_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'user_email': self.user.email if self.user else None,
            'bicycle_id': self.bicycle_id,
            'bicycle_number': self.bicycle.bicycle_number if self.bicycle else None,
            'bicycle_type': self.bicycle.type if self.bicycle else None,
            'rental_rate': float(self.bicycle.rental_rate) if self.bicycle and self.bicycle.rental_rate is not None else 0.0,
            'start_station_id': self.start_station_id,
            'start_station_name': self.start_station.station_name if self.start_station else None,
            'return_station_id': self.return_station_id,
            'return_station_name': self.return_station.station_name if self.return_station else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'return_time': self.return_time.isoformat() if self.return_time else None,
            'duration': float(self.duration) if self.duration is not None else None,
            'fare': float(self.fare) if self.fare is not None else None,
            'status': self.status,
            'payment_status': self.payment.status if self.payment else ('Pending' if self.status == 'Active' else 'Paid')
        }

