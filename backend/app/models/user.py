from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.orm import relationship
from app.extentions.database import Base
from datetime import datetime, timedelta

class UserModel(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(26), unique=True, index=True)
    password = Column(String(256))
    role = Column(String(10), default="developer")
    created_at = Column(DateTime, default=datetime.utcnow)
    expired_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=90))


    secrets = relationship("SecretsModel", back_populates="owner")
    audit_logs = relationship("AuditModel", back_populates="owner")