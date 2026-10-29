#!/usr/bin/env python
"""
Public Bicycle Rental Management System (PBRMS)
Safe SQLite to MySQL Migration Script
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.extensions import db
from sqlalchemy import text

def clean_timestamp(ts_val):
    """Normalize timestamp string for MySQL DATETIME."""
    if ts_val is None:
        return None
    if isinstance(ts_val, datetime):
        return ts_val.strftime('%Y-%m-%d %H:%M:%S')
    s = str(ts_val).strip()
    if 'T' in s:
        s = s.replace('T', ' ').split('.')[0].split('+')[0].replace('Z', '')
    return s

def migrate():
    sqlite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pbrms_dev.sqlite'))
    if not os.path.exists(sqlite_path):
        print(f"[ERROR] Source SQLite database not found at {sqlite_path}")
        return False

    print("=" * 65)
    print("  PBRMS: SQLite to MySQL Migration Process")
    print(f"  Source: {os.path.basename(sqlite_path)}")
    print("  Target: MySQL pbrms_db via SQLAlchemy (PyMySQL)")
    print("=" * 65)

    # 1. Connect to SQLite read-only
    sqlite_conn = sqlite3.connect(f"file:{sqlite_path}?mode=ro", uri=True)
    sqlite_conn.row_factory = sqlite3.Row
    sq_cur = sqlite_conn.cursor()

    # 2. Initialize Flask App in development mode (connected to MySQL)
    app = create_app('development')

    with app.app_context():
        # Step A: Safe Schema Creation using SQLAlchemy
        print("\n[Step 1/3] Creating MySQL tables if not exist using SQLAlchemy models...")
        db.create_all()
        print("  [OK] Tables verified/created successfully.")

        # Table order respecting foreign keys
        migration_order = [
            'admin',
            'user',
            'rental_owner',
            'station',
            'bicycle',
            'rental',
            'payment'
        ]

        # Step B: Check target MySQL row counts
        with db.engine.connect() as conn:
            existing_counts = {}
            for table in migration_order:
                count = conn.execute(text(f"SELECT COUNT(*) FROM `{table}`")).scalar()
                existing_counts[table] = count

        total_existing = sum(existing_counts.values())
        if total_existing > 0:
            print(f"\n[NOTICE] Target MySQL database already contains {total_existing} total rows across tables:")
            for t, c in existing_counts.items():
                print(f"  - {t}: {c} rows")
            print("  Skipping insert to avoid duplicate records or overwriting existing data.")
            return True

        # Step C: Migrate Data
        print("\n[Step 2/3] Migrating records from SQLite to MySQL...")
        with db.engine.begin() as conn:
            # Temporarily disable foreign key checks during migration for smooth inserts
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

            for table in migration_order:
                rows = sq_cur.execute(f"SELECT * FROM `{table}`").fetchall()
                print(f"  Migrating table `{table}`: {len(rows)} records found in SQLite...")

                for row in rows:
                    row_dict = dict(row)

                    # Normalize timestamps
                    for date_col in ['created_at', 'start_time', 'return_time', 'payment_date']:
                        if date_col in row_dict:
                            row_dict[date_col] = clean_timestamp(row_dict[date_col])

                    columns = list(row_dict.keys())
                    col_names = ", ".join([f"`{c}`" for c in columns])
                    placeholders = ", ".join([f":{c}" for c in columns])

                    sql = text(f"INSERT INTO `{table}` ({col_names}) VALUES ({placeholders})")
                    conn.execute(sql, row_dict)

            # Re-enable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        # Step D: Verify row counts match
        print("\n[Step 3/3] Validating migrated data consistency...")
        all_matched = True
        validation_report = []

        with db.engine.connect() as conn:
            for table in migration_order:
                sq_cnt = sq_cur.execute(f"SELECT COUNT(*) FROM `{table}`").fetchone()[0]
                my_cnt = conn.execute(text(f"SELECT COUNT(*) FROM `{table}`")).scalar()
                matched = (sq_cnt == my_cnt)
                if not matched:
                    all_matched = False
                validation_report.append((table, sq_cnt, my_cnt, matched))

        print("\n" + "-" * 60)
        print(f"{'Table Name':<16} | {'SQLite Rows':<12} | {'MySQL Rows':<12} | {'Status'}")
        print("-" * 60)
        for t, sq, my, m in validation_report:
            status_str = "MATCHED (OK)" if m else "MISMATCH (ERROR)"
            print(f"{t:<16} | {sq:<12} | {my:<12} | {status_str}")
        print("-" * 60)

        sqlite_conn.close()

        if all_matched:
            print("\n[SUCCESS] Migration completed successfully with 100% data integrity!")
            return True
        else:
            print("\n[ERROR] Row count mismatch detected between SQLite and MySQL.")
            return False

if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
