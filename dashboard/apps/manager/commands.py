from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from apps.authentication.models import Users
from apps.home.models import MenuItem 
from apps import db

cli = AppGroup("manager")

@cli.command("create-default-manager")
def create_default_manager():
    """Create a default manager account."""
    username = "admin"
    email = "admin@example.com"
    password = generate_password_hash("admin")
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
        {"name": "Chicken Wings", "price": 10.99, "image_file": "7e80f6423296bbeegit ad.jpg"},
        {"name": "Halloumi Chips", "price": 10.99, "image_file": "8d81d750370a6d03.jpg"},
        {"name": "Supremo Wrap", "price": 14.99, "image_file": "9ea01ea9aff9e2b7.jpg"},
        {"name": "Chicken Burger Meal", "price": 19.99, "image_file": "34dd7897dd27f230.jpg"},
        {"name": "Cheesy Garlic Pita", "price": 9.99, "image_file": "82a5603205aa2953.jpg"},
        {"name": "Chocolate Mousse", "price": 4.99, "image_file": "8512514343ce84af.jpg"},
        {"name": "Family Chicken Meal", "price": 24.99, "image_file": "a8ef2e71090ea2c9.jpg"},
        {"name": "Paella", "price": 14.99, "image_file": "a85209377ddfc90b.jpg"},
        {"name": "Chicken Avocado Salad", "price": 11.99, "image_file": "a517464516f134bd.png"},
        {"name": "Hummus and Pita", "price": 9.99, "image_file": "b8aeee58e8aff162.png"}
    ]

    for item in menu_items:
        if not MenuItem.query.filter_by(name=item["name"]).first():
            menu_item = MenuItem(name=item["name"], description=item["description"], price=item["price"])
            db.session.add(menu_item)
            db.session.commit()
            print(f"Menu item '{item['name']}' created.")
        else:
            print(f"Menu item '{item['name']}' already exists.")