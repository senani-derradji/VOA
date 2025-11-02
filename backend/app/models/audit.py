from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.extentions.database import Base
from datetime import datetime



class AuditModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_table.id"))
    action = Column(String, default="create")
    timestamp = Column(DateTime, default=datetime.utcnow())
    integrity_checks = Column(String(512))

    owner = relationship("UserModel", back_populates="audit_logs")