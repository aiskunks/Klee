from klee_engine.application.config import BASE_DIR, ROOT_DIR, SECRETS

DB_URI_FORMAT = "postgresql+psycopg2://{username}:{password}@{url}:{db_port}/{db}"


class BackendSettings:
    # Header application settings:
    SECRET_KEY = SECRETS["SECRET_KEY"]
    # Header paths:
    ROOT_DIR = ROOT_DIR
    BASE_DIR = BASE_DIR
    # Static and media files:
    DATA_DIR = f"{ROOT_DIR}/data"
    STATIC_DIR = f"{BASE_DIR}/static"
    DATA_URL = "/data/"
    STATIC_URL = "/static/"
    # Database:
    SQLALCHEMY_DATABASE_URI = DB_URI_FORMAT.format(
        username=SECRETS["DB_USERNAME"],
        password=SECRETS["DB_PASSWORD"],
        url=SECRETS["DB_URL"],
        db_port=SECRETS["DB_PORT"],
        db=SECRETS["DB_NAME"],
    )
    # Admin:
    FLASK_ADMIN_SWATCH = "flatly"
