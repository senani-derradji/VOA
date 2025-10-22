from app.core.database import SessionLocal, engine, Base
from app.models.user import UserModel as User
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()

admin_username = "adminderradji"
admin_password = "Admin@PassWord.1+1"

existing_user = db.query(User).filter(User.username == admin_username).first()

if existing_user: print(f"Admin '{admin_username}' already exists.")
else:
    print ("Create ADMIN ....")
    user = User(username=admin_username, 
               password=get_password_hash(admin_password), 
               role="admin")
    db.add(user)
    db.commit()
    db.close()

print(f"""
\n\nINFO :
    username: {admin_username}
    password: {admin_password}\n\n
""")