from app import app, db
from werkzeug.security import generate_password_hash
from Db.models import User

admin_name = "Admin"
admin_login = "Admin"
admin_password = "Admin"

with app.app_context():
    hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')
    new_admin = User(username=admin_name, password=hashed_password, is_admin=True)

    existing_admin = User.query.filter_by(username=admin_login).first()
    if existing_admin:
        print("Админ уже есть!")
    else:
        db.session.add(new_admin)
        db.session.commit()
        print(f"Админ {admin_name} сделан.")
