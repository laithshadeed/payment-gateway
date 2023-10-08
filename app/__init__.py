from flask import Flask
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics

import logging

from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  # Initialize Flask extensions
  db.init_app(app)
  migrate = Migrate(app, db)
  Talisman(app)
  metrics = PrometheusMetrics(app)

  logging.basicConfig(level=logging.INFO)

  from app.payments_api import payments_api
  from app.server_api import server_api

  limiter = Limiter(key_func=get_remote_address, app=app, default_limits = ["1000/minute, 100/second"])
  limiter.limit("60/minute, 1/second")(payments_api)
  limiter.limit("6000/minute, 100/second")(server_api)

  app.register_blueprint(payments_api, url_prefix='/api/v1/payments')
  app.register_blueprint(server_api, url_prefix='/')

  return app
