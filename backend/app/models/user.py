from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserModel(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(26), unique=True, index=True)
    password = Column(String(256))
    role = Column(String(10), default="developer")

    secrets = relationship("SecretsModel", back_populates="owner")
    audit_logs = relationship("AuditModel", back_populates="owner")