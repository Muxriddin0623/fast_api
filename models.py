from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from datetime import datetime
from enum import Enum as PyEnum
from database import Base

class DebtType(PyEnum):
    OWED_TO = "owed_to"
    OWED_BY = "owed_by"

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, default="UZS")
    reminder_time = Column(Integer, default=24)  # in hours

class Debt(Base):
    __tablename__ = "debts"
    id = Column(Integer, primary_key=True, index=True)
    debt_type = Column(Enum(DebtType), nullable=False)
    person_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    description = Column(String)
    date_time = Column(DateTime, default=datetime.utcnow)
    due_date_time = Column(DateTime)