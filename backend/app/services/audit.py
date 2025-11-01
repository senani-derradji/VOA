from app.models.audit import AuditModel
from sqlalchemy.orm import Session
from app.schemas.audit import Action

def log_action(db: Session,
               user_id : int,
               action : Action
               ):
    log = AuditModel(user_id=user_id,action=action)
    try:
        db.add(log)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Failed to commit audit log: {e}")

    print(f"Audit log created: User ID {user_id}, Action: {action}")