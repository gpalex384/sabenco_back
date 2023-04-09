from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome!"}

# Get the events of a category starting between two dates
@app.get("/events/{startdate}/{enddate}/{category}", response_model = List[schemas.Event])
def read_events_by_dates_and_category(startdate: str, enddate: str, category: str, db: Session = Depends(get_db)):
    db_event_by_category = crud.get_event_by_category(db, startdate=startdate, enddate=enddate, category=category)
    return db_event_by_category

# Get the user data given the userId
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Create an event draft given the title, detail, start date, end date and publication requested
@app.post("/users/{user_id}/events", response_model = schemas.EventBase)
def create_event_by_user(event:schemas.EventBase, user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_created_event = crud.create_event(db, event, user_id)
    return db_created_event
