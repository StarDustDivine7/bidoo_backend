from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class Attendance(Base):
    """Ek user ka ek din ka attendance lifecycle yaha store hota hai."""

    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    attendance_date = Column(Date, nullable=False, index=True, default=date.today)
    check_in_time = Column(DateTime, nullable=True)
    lunch_start_time = Column(DateTime, nullable=True)
    lunch_end_time = Column(DateTime, nullable=True)
    check_out_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="attendance_records")
