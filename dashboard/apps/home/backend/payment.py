"""
  payment.py
  ===================

  Description:          Payment related code.
  Authors:              Duhncan Guy
  Creation Date:        2024-05-01
  Modification Date:    2024-05-01

"""

from datetime import datetime

from . import order


class Payment:
    def __init__(self, customer: str, order: order.Order):
        self.customer = customer
        self.order = order
        self.amount_paid = 0
        self.time = datetime.now()


class CashPayment(Payment):
    def calculate_change(self, cash_given: int):
        return cash_given - self.amount_paid


class CardPayment(Payment):
    def __init__(self, customer: str, order: order.Order, card_details: list):
        super().__init__(customer, order)
        self.card_details = card_details
