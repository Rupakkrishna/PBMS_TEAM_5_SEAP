#!/usr/bin/env python
"""
Public Bicycle Rental Management System (PBRMS)
Application Entry Point & Runner
"""

import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.database.db import init_db_schema
from backend.database.seed import seed_database

def main():
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)

    # CLI Flags
    if '--init-db' in sys.argv:
        with app.app_context():
            print("Initializing database schema...")
            init_db_schema()
            print("Database schema initialized.")
        return

    if '--seed' in sys.argv:
        with app.app_context():
            print("Seeding database with demo data...")
            seed_database()
            print("Database seeded.")
        return

    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    debug = app.config.get('DEBUG', True)

    print("=" * 65)
    print("  Public Bicycle Rental Management System (PBRMS)")
    print("  SEAP Jira Project Traceability: Sprints 1-4 (PB-01 - PB-24)")
    print(f"  Server running on http://{host}:{port}")
    print("=" * 65)

    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()

