from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.extentions.database import Base
from datetime import datetime, timedelta


class SecretsModel(Base):
    __tablename__ = "secrets_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), index=True)
    value = Column(String(1024))
    environment = Column(String(4), default="dev")
    created_at = Column(DateTime, default=datetime.utcnow)
    expired_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=1))

    owner_id = Column(Integer, ForeignKey("users_table.id"))
    owner = relationship("UserModel", back_populates="secrets")
    versions = relationship("SecretVersionModel", back_populates="secret", cascade="all, delete-orphan")


class SecretVersionModel(Base):
    __tablename__ = "secret_versions"

    id = Column(Integer, primary_key=True, index=True)
    secret_id = Column(Integer, ForeignKey("secrets_table.id"))
    value = Column(String(1024))
    created_at = Column(DateTime, default=datetime.utcnow)
    # expired_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(seconds=10))

    version_number = Column(Integer, default=1)

    secret = relationship("SecretsModel", back_populates="versions")
