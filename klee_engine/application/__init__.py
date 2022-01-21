import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../", "../")))

from klee_engine.application.settings import BackendSettings

backend_application = Flask(
    import_name=__name__, template_folder=f"{BackendSettings.BASE_DIR}/templates/"
)
backend_application.config.from_object(BackendSettings)
db = SQLAlchemy(backend_application)
migrate = Migrate(backend_application, db)
login_manager = LoginManager(backend_application)
CORS(
    backend_application,
    supports_credentials=True,
    allow_headers="*",
    resources={r"/*": {"origins": "*"}}
)

from klee_engine import models
from klee_engine import api
