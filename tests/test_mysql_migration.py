"""
Integration tests verifying MySQL 8.0 connectivity and database integrity on pbrms_db.
"""

import pytest
from backend.app import create_app
from backend.extensions import db
from backend.models import User, Admin, RentalOwner, Station, Bicycle, Rental, Payment

@pytest.fixture(scope="module")
def mysql_app():
    """Create app connected to MySQL development database."""
    app = create_app('development')
    with app.app_context():
        yield app

def test_mysql_connection_and_models(mysql_app):
    """Verify SQLAlchemy ORM queries execute cleanly against MySQL pbrms_db."""
    with mysql_app.app_context():
        # Verify Admins
        admins = Admin.query.all()
        assert len(admins) >= 1
        assert any(a.email == 'admin@pbrms.com' for a in admins)

        # Verify Users
        users = User.query.all()
        assert len(users) >= 2
        assert any(u.email == 'alice@example.com' for u in users)
        assert any(u.email == 'bob@example.com' for u in users)

        # Verify Rental Owners
        owners = RentalOwner.query.all()
        assert len(owners) >= 3
        assert any(o.approval_status == 'Approved' for o in owners)
        assert any(o.approval_status in ['Approved', 'Pending', 'Rejected'] for o in owners)

        # Verify Stations
        stations = Station.query.all()
        assert len(stations) >= 4
        for s in stations:
            assert s.capacity > 0
            assert s.available_bicycles >= 0

        # Verify Bicycles & Relationships
        bicycles = Bicycle.query.all()
        assert len(bicycles) >= 8
        for b in bicycles:
            assert b.owner is not None  # FK relationship to rental_owner verified
            assert b.rental_rate >= 0

        # Verify Rentals & Payments
        rentals = Rental.query.all()
        assert len(rentals) >= 2
        for r in rentals:
            assert r.user is not None  # FK relationship to user verified
            assert r.bicycle is not None  # FK relationship to bicycle verified

        payments = Payment.query.all()
        assert len(payments) >= 1
        for p in payments:
            assert p.rental is not None  # FK relationship to rental verified
            assert p.amount > 0
