"""
  restaraunt.py
  ===================

  Description:          Restaraunt logic.
  Authors:              Duhncan Guy
  Creation Date:        2024-05-01
  Modification Date:    2024-05-01

"""

from . import menu


class Restaraunt:
    def __init__(self):
        self.current_orders = []
        self.staff_on_duty = []
        self.available_tables = []
        self.active_menu = menu.Menu()
