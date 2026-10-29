import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.extensions import db
from sqlalchemy import text

app = create_app('development')

with app.app_context():
    has_host = bool(app.config.get('DB_HOST'))
    has_user = bool(app.config.get('DB_USER'))
    has_pwd = bool(app.config.get('DB_PASSWORD'))
    db_name = app.config.get('DB_NAME')
    use_sqlite = app.config.get('USE_SQLITE_FALLBACK')

    print(f"ENV_LOADED: DB_HOST_SET={has_host}, DB_USER_SET={has_user}, DB_PWD_SET={has_pwd}")
    print(f"TARGET_DATABASE={db_name}")
    print(f"USE_SQLITE_FALLBACK={use_sqlite}")

    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE(), VERSION()")).fetchone()
            current_db, version = result[0], result[1]
            print("CONNECTION_SUCCESS=True")
            print(f"CONNECTED_DATABASE={current_db}")
            print(f"SERVER_VERSION={version}")
            print(f"MATCHES_PBRMS_DB={current_db == 'pbrms_db'}")
    except Exception as e:
        print("CONNECTION_SUCCESS=False")
        print(f"ERROR_TYPE={type(e).__name__}")
        # Sanitize any password from error message
        err_str = str(e)
        if "://" in err_str:
            err_str = err_str.split("://")[0] + "://[REDACTED]"
        print(f"ERROR_MESSAGE={err_str}")
