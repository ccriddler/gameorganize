from . import create_app
from .db import db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)