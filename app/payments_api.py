from flask import request, jsonify, abort
from flask import Blueprint
from werkzeug.exceptions import BadRequest, HTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.extensions import db
from app.utils import bank_simulator
from app.payments_model import Payment

payments_api = Blueprint('payments_api', __name__)

def validate_payment_input(data):
  required_fields = ['idempotency_key', 'card_number', 'amount', 'expiry_date', 'currency', 'cvv']
  for field in required_fields:
    if field not in data:
      raise BadRequest(f'Missing {field} field')
  # TODO: Add more validation, like verifying the format of card number, etc.

# TODO: Add pagination, filtering & page limit
@payments_api.route('', methods=['GET'])
def get_all_payments():
  payments = Payment.query.all()
  return jsonify([{
    'payment_id': payment.id,
    'idempotency_key': payment.idempotency_key,
    'masked_card_number': payment.masked_card_number,
    'expiry_date': payment.expiry_date,
    'amount': payment.amount,
    'currency': payment.currency,
    'status': payment.status,
    'created_at': payment.created_at
  } for payment in payments])


@payments_api.route('', methods=['POST'])
def create_payment():
  data = request.get_json()

  try:
    validate_payment_input(data)
  except BadRequest as e:
    return abort(400, description=str(e))

  idempotency_key = data['idempotency_key']
  existing_payment = Payment.query.filter_by(idempotency_key=idempotency_key).first()
  if existing_payment:
    logging.info('Payment already exists with id: %s, idempotency_key: %s and card: %s', existing_payment.id, existing_payment.idempotency_key, existing_payment.masked_card_number)
    return jsonify({
      'payment_id': existing_payment.id,
      'idempotency_key': existing_payment.idempotency_key,
      'status': existing_payment.status
    })


  card_number = data['card_number']
  amount = data['amount']
  expiry_date = data['expiry_date']
  currency = data['currency']
  cvv = data['cvv']

  bank_response = bank_simulator(card_number, amount, expiry_date, currency, cvv)

  payment = Payment(
    idempotency_key=idempotency_key,
    masked_card_number=card_number[-4:].rjust(len(card_number), '*'),
    expiry_date=expiry_date,
    amount=amount,
    currency=currency,
    status=bank_response
  )

  try:
    db.session.add(payment)
    db.session.commit()
  except SQLAlchemyError as e:
    db.session.rollback()
    logging.error("Database Error: %s", e)
    return abort(500, description="Internal Server Error")

  logging.info('Payment created with id: %s and card: %s', payment.id, payment.masked_card_number)

  return jsonify({
    'payment_id': payment.id,
    'status': payment.status
  })

@payments_api.route('<payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
  payment = Payment.query.get(payment_id)
  if not payment:
    return abort(404, description='Payment not found')

  try:
    db.session.delete(payment)
    db.session.commit()
  except SQLAlchemyError as e:
    db.session.rollback()
    logging.error("Database Error: %s", e)
    return abort(500, description="Internal Server Error")

  logging.info('Payment deleted with id: %s and card: %s', payment.id, payment.masked_card_number)

  return jsonify({
    'payment_id': payment_id,
    'status': 'deleted'
  })

@payments_api.route('<payment_id>', methods=['GET'])
def get_payment(payment_id):
  payment = Payment.query.get(payment_id)
  if not payment:
    return abort(404, description='Payment not found')

  return jsonify({
    'payment_id': payment.id,
    'idempotency_key': payment.idempotency_key,
    'masked_card_number': payment.masked_card_number,
    'expiry_date': payment.expiry_date,
    'amount': payment.amount,
    'currency': payment.currency,
    'status': payment.status,
    'created_at': payment.created_at
  })

@payments_api.app_errorhandler(HTTPException)
def handle_exception(e):
    logging.error(e)
    return jsonify(error=str(e.description)), e.code
