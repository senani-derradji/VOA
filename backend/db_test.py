from app.core.database import SessionLocal, engine, Base
from app.models.user import UserModel as User
from app.models.secrets import SecretsModel as Secrets
from app.models.audit import AuditModel as Audit
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()

admin_username = "adminderradji"
admin_password = "Admin@PassWord.1+1"
developer_username = "devinderradji"
developer_password = "Dev@PassWord.1+1"


existing_admin = db.query(User).filter(User.username == admin_username).first()
existing_developer = db.query(User).filter(User.username == developer_username).first()

if existing_admin and existing_developer: print(f"Admin \ Developer '{admin_username} \ {developer_username} ' already exists.")
else:
    print ("CREATING ADMIN \ DEVELOPER IN PROGESS ....")

    admin = User(username=admin_username, 
               password=get_password_hash(admin_password), 
               role="admin")
    developer = User(username=developer_username, 
               password=get_password_hash(developer_password), 
               role="developer")
    
    db.add(admin)
    db.commit()
    db.refresh(admin)

    db.add(developer)
    db.commit()
    db.refresh(developer)

    db.close()

print(f"""
\n\nINFO :
    admin_username: {admin_username}
    admin_password: {admin_password}

    dev_username: {developer_username}
    dev_password: {developer_password}\n\n
""")