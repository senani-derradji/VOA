from app.models.audit import AuditModel

def log_action(db, user_id: int, action: str):
    log = AuditModel(
        user_id=user_id, 
        action=action
        )
    db.add(log)
    db.commit()