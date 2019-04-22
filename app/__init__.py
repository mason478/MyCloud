from flask import Flask
from app.api_v1 import api_v1
from config import config


def create_app(config_name):
    config[config_name].start_hook()
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    app.config.from_object(config[config_name])  # read configs from config.py
    config[config_name].init_app(app)

    return app
