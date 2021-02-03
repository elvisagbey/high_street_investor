from app import create_app, db
from config import config

from flask_migrate import Migrate


app = create_app(config.get('default'))

migrate = Migrate(app, db)
