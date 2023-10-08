def bank_simulator  (card_number, amount, expiry_date, currency, cvv):
  if int(card_number[-1]) % 2 == 0:
    return 'Success'
  return 'Failure'
