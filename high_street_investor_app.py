from app import create_app
from config import config


create_app(config.get('default'))
