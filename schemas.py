from pydantic import BaseModel
from datetime import datetime
from models import *
class SettingsSchema(BaseModel):
    currency: str
    reminder_time: int

    class Config:
        orm_mode = True

class DebtSchema(BaseModel):
    debt_type: DebtType
    person_name: str
    amount: float
    currency: str
    description: str
    date_time: datetime
    due_date_time: datetime

    class Config:
        orm_mode = True
