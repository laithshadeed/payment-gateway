from datetime import datetime
from app.extensions import db

class Payment(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  idempotency_key = db.Column(db.String, nullable=True)
  __table_args__ = (db.UniqueConstraint('idempotency_key',  name='unique_idempotency_key'),)
  masked_card_number = db.Column(db.String, nullable=False)
  expiry_date = db.Column(db.String, nullable=False)
  amount = db.Column(db.String, nullable=False)
  currency = db.Column(db.String, nullable=False)
  status = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
