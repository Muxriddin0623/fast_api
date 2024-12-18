from schemas import *
from models import *
from fastapi import APIRouter, HTTPException, Depends
from database import *
from sqlalchemy.exc import IntegrityError

application = APIRouter(
    prefix="/",
)

session = session(bind=engine)

@application.get("/api/settings/", response_model=SettingsSchema)
def get_settings(db: SessionLocal = Depends(get_db)):
    settings = db.query(Settings).first()
    if not settings:
        settings = Settings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@application.put("/api/settings/", response_model=SettingsSchema)
def update_settings(settings: SettingsSchema, db: SessionLocal = Depends(get_db)):
    current_settings = db.query(Settings).first()
    if not current_settings:
        current_settings = Settings()
        db.add(current_settings)
    current_settings.currency = settings.currency
    current_settings.reminder_time = settings.reminder_time
    db.commit()
    db.refresh(current_settings)
    return current_settings

@application.get("/api/monitoring/")
def get_monitoring(db: SessionLocal = Depends(get_db)):
    total_owed_to = db.query(Debt).filter(Debt.debt_type == DebtType.OWED_TO).count()
    total_owed_by = db.query(Debt).filter(Debt.debt_type == DebtType.OWED_BY).count()
    balance = total_owed_by - total_owed_to
    return {
        "total_owed_to": total_owed_to,
        "total_owed_by": total_owed_by,
        "balance": balance
    }

@application.post("/api/debts/", response_model=DebtSchema)
def add_debt(debt: DebtSchema, db: SessionLocal = Depends(get_db)):
    new_debt = Debt(**debt.dict())
    db.add(new_debt)
    try:
        db.commit()
        db.refresh(new_debt)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Debt could not be added.")
    return new_debt

@application.put("/api/debts/{debt_id}/", response_model=DebtSchema)
def update_debt(debt_id: int, debt: DebtSchema, db: SessionLocal = Depends(get_db)):
    existing_debt = db.query(Debt).filter(Debt.id == debt_id).first()
    if not existing_debt:
        raise HTTPException(status_code=404, detail="Debt not found.")
    for key, value in debt.dict().items():
        setattr(existing_debt, key, value)
    db.commit()
    db.refresh(existing_debt)
    return existing_debt

@application.delete("/api/debts/{debt_id}/")
def delete_debt(debt_id: int, db: SessionLocal = Depends(get_db)):
    existing_debt = db.query(Debt).filter(Debt.id == debt_id).first()
    if not existing_debt:
        raise HTTPException(status_code=404, detail="Debt not found.")
    db.delete(existing_debt)
    db.commit()
    return {"detail": "Debt deleted successfully."}

@application.get("/api/debts/")
def list_debts(debt_type: DebtType  = None, db: SessionLocal = Depends(get_db)):
    query = db.query(Debt)
    if debt_type:
        query = query.filter(Debt.debt_type == debt_type)
    return query.all()