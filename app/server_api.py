from flask import jsonify
from flask import Blueprint
from werkzeug.exceptions import HTTPException
from sqlalchemy import text
from datetime import datetime
import logging

from app.extensions import db

server_api = Blueprint('server_api', __name__)

@server_api.route('/status', methods=['GET'])
def status():
  try:
    db.session.execute(text('SELECT 1'))
    db_status = 'connected'
  except Exception as e:
    logging.error(e)
    db_status = 'disconnected'

  return jsonify(status='running', db_status=db_status)

@server_api.route('/info', methods=['GET'])
def info():
  # TODO: Make this dynamic
  return jsonify(
      version='1.0.0',
      build_date='01-01-2023',
      commit_hash='abcd1234'
  )

@server_api.route('/version', methods=['GET'])
def version():
  # TODO: Make this dynamic
  return jsonify(version='1.0.0')

@server_api.route('/health', methods=['GET'])
def health():
  return jsonify(status='healthy')

@server_api.route('/ping', methods=['GET'])
def ping():
  return jsonify(status='pong')

@server_api.route('/time', methods=['GET'])
def time():
  return jsonify(server_time_utc=datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"))

@server_api.route('/docs', methods=['GET'])
def docs():
  # TODO: Redirect to a Swagger UI or Redoc page.
  return jsonify(message="API Documentation can be found at [URL]")

@server_api.app_errorhandler(HTTPException)
def handle_exception(e):
    logging.error(e)
    return jsonify(error=str(e.description)), e.code


