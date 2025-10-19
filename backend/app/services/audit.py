from app.models.audit import AuditModel
from app.schemas.audit import AuditOut

def log_action(db, 
               data_form = AuditOut
               ):
    user_id = data_form.user_id
    action = data_form.action
    log = AuditModel(
        user_id=user_id, 
        action=action
        )
    db.add(log)
    db.commit()