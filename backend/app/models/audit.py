from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column
from app.core.database import Base
from app.utils.TimeNow import time_


class AuditModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_table.id"))
    action = Column(String(10), default="create")
    timestamp = Column(DateTime, default=time_)

    owner = relationship("UserModel", back_populates="audit_logs")