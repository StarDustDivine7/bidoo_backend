from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class WorkLog(Base):
    """User ne aaj kya kaam kiya uska daily update yaha rahega."""

    __tablename__ = "work_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    work_date = Column(Date, nullable=False, index=True, default=date.today)
    summary = Column(Text, nullable=False)
    blockers = Column(Text, nullable=True)
    hours_spent = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="work_logs")
