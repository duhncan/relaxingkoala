from flask.cli import AppGroup
from apps.authentication.util import hash_pass

from apps.authentication.models import Users
from apps.home.models import MenuItem 
from apps import db

cli = AppGroup("manager")

@cli.command("create-default-manager")
def create_default_manager():
    """Create a default manager account."""
    username = "admin"
    email = "admin@example.com"
    password = "admin"
    hash_password = hash_pass(password)
    role = "manager"

    if not Users.query.filter_by(username=username).first():
        default_manager = Users(username=username, email=email, password=password, role=role)
        db.session.add(default_manager)
        db.session.commit()
        print("Default manager account created.")
    else:
        print("Manager account already exists.")

@cli.command("create-default-menu-items")
def create_default_menu_items():
    """Create 10 default menu items."""
    menu_items = [
        {"name": "Chicken Wings", "price": 10.99, "image_file": "chickenmeal.png"},
        {"name": "Halloumi Chips", "price": 10.99, "image_file": "halloumi.png"},
        {"name": "Supremo Wrap", "price": 14.99, "image_file": "supremo.png"},
        {"name": "Chicken Burger Meal", "price": 19.99, "image_file": "chickenburger.png"},
        {"name": "Cheesy Garlic Pita", "price": 9.99, "image_file": "cheesygarlic.png"},
        {"name": "Chocolate Mousse", "price": 4.99, "image_file": "mousse.png"},
        {"name": "Family Chicken Meal", "price": 24.99, "image_file": "familychicken.png"},
        {"name": "Paella", "price": 14.99, "image_file": "paella.png"},
        {"name": "Chicken Avocado Salad", "price": 11.99, "image_file": "chickenavocado.png"},
        {"name": "Hummus and Pita", "price": 9.99, "image_file": "hummus.png"}
    ]

    for item in menu_items:
        if not MenuItem.query.filter_by(name=item["name"]).first():
            menu_item = MenuItem(name=item["name"], price=item["price"], image_file=item["image_file"])
            db.session.add(menu_item)
            db.session.commit()
            print(f"Menu item '{item['name']}' created.")
        else:
            print(f"Menu item '{item['name']}' already exists.")