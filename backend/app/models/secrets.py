from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.TimeNow import time_

class SecretsModel(Base):
    __tablename__ = "secrets_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), index=True)
    value = Column(String)
    environment = Column(String(4), default="dev")
    created_at = Column(DateTime, default=time_)
    
    owner_id = Column(Integer, ForeignKey("users_table.id"))
    owner = relationship("UserModel", back_populates="secrets")