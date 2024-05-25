from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from apps.authentication.models import Users
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