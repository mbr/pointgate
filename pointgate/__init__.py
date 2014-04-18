from flask import Flask
from flask.ext.appconfig import HerokuConfig
from pointgate.dyndnsapi import dyndnsapi


def create_app(configfile=None):
    app = Flask(__name__)

    HerokuConfig(app, configfile)
    app.config.setdefault('POINTDNS_API_URL', 'https://pointhq.com')
    app.config.setdefault('POINTDNS_RECORD_TTL', 60)

    app.register_blueprint(dyndnsapi)

    return app
