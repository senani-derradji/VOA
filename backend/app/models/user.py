from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserModel(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(10), unique=True, index=True)
    password = Column(String)
    role = Column(String(10), default="user")

    secrets = relationship("SecretsModel", back_populates="owner")
    audit_logs = relationship("AuditModel", back_populates="owner")