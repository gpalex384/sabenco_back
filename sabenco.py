from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/events/{startdate}/{enddate}/{category}", response_model = List[schemas.Event])
def read_events_by_dates_and_category(startdate: str, enddate: str, category: str, db: Session = Depends(get_db)):
    db_event_by_category = crud.get_event_by_category(db, startdate=startdate, enddate=enddate, category=category)
    return db_event_by_category