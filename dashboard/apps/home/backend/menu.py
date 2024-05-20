"""
  menu.py
  ===================

  Description:          Menu related classes allowed to be selected by users to input to order.
  Authors:              Duhncan Guy
  Creation Date:        2024-05-01
  Modification Date:    2024-05-01

"""

from typing import Literal, List
import apps.home.models as models

MenuItem = models.MenuItem

class Menu:
    type: Literal["Breakfast", "Lunch", "Dinner"]
    items: List[MenuItem]

    def __init__(self, type: Literal["Breakfast", "Lunch", "Dinner"],
                 items: List[MenuItem]):
        self.type = type
        self.items = items
