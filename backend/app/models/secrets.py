from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class SecretsModel(Base):
    __tablename__ = "secrets_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), index=True)
    value = Column(String)
    environment = Column(String(4), default="dev")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users_table.id"))
    owner = relationship("UserModel", back_populates="secrets")