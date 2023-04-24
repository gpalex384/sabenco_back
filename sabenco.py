import datetime
from typing import List, Union
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

# Get the events of a category which startdate is between two dates
@app.get("/events/{category_id}/{startdate}/{enddate}", response_model = List[schemas.Event])
def read_events_by_dates_and_category(category_id: str, startdate: str, enddate: str, db: Session = Depends(get_db)):
    try:
        datetime.date.fromisoformat(startdate)
        datetime.date.fromisoformat(enddate)
    except ValueError:
        raise HTTPException(status_code=401, detail="Incorrect data format, should be YYYY-MM-DD")
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_event_by_category = crud.get_event_by_category(db, category_id=category_id, startdate=startdate, enddate=enddate)
    return db_event_by_category

# Get the user data given the userId
#TODO encrypt password 
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get event drafts created by user (not posted / pending moderation)
@app.get("/users/{user_id}/eventdrafts", response_model=List[schemas.EventDraft])
def read_event_drafts_by_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_eventdraft = crud.get_eventdraft_by_user_id(db, user_id)
    return db_eventdraft


# Create an event draft given the title, detail, start date, end date and publication requested
@app.post("/users/{user_id}/eventdraft", response_model = schemas.EventDraftBase)
def create_event_draft(eventdata:schemas.EventDraftBase, user_id: str, event_id: Union[str,None] = None, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if event_id:
        db_event = crud.get_event_by_id(db, event_id=event_id)
        if db_event is None:
            raise HTTPException(status_code=404, detail="Event not found")        
    db_created_eventdraft = crud.create_eventdraft(db, eventdata, user_id, event_id)
    return db_created_eventdraft

# Create an event draft given the title, detail, start date, end date and publication requested
@app.put("/users/{user_id}/eventdraft/{eventdraft_id}", response_model = schemas.EventDraft)
def edit_event_draft(eventdata:schemas.EventDraftBase, user_id: str, eventdraft_id: str, db: Session = Depends(get_db)):
    # Exception control
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_eventdraft = crud.get_eventdraft_by_id(db, eventdraft_id)
    if db_eventdraft is None:
        raise HTTPException(status_code=404, detail="Event draft not found")
    db_edited_eventdraft = crud.edit_eventdraft(db, eventdata, user_id, db_eventdraft)
    return db_edited_eventdraft

# Accept an event draft, making it become a published event
@app.post("/users/{user_id}/events/publish/{eventdraft_id}", response_model = schemas.Event)
def publish_event(eventdraft_id: str, user_id: str, db: Session = Depends(get_db)):
    # Exception control
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_eventdraft = crud.get_eventdraft_by_id(db, eventdraft_id=eventdraft_id)
    if db_eventdraft is None:
        raise HTTPException(status_code=404, detail="Event draft not found")
    # Publish eventdraft
    db_published_event = crud.publish_eventdraft(db, eventdraft_id, user_id)
    return db_published_event

# Reject an event draft, adding a comment from the moderator
@app.put("/users/{user_id}/events/reject/{eventdraft_id}", response_model = schemas.EventDraft)
def reject_event(comment: str, eventdraft_id: str, user_id: str, db: Session = Depends(get_db)):
    # Exception control
    if comment is None or comment == '':
        raise HTTPException(status_code=401, detail="The comment is required for rejecting")
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_eventdraft = crud.get_eventdraft_by_id(db, eventdraft_id=eventdraft_id)
    if db_eventdraft is None:
        raise HTTPException(status_code=404, detail="Event draft not found")
    # Edit eventdraft
    db_rejected_event = crud.reject_eventdraft(db, db_eventdraft, user_id, comment)
    return db_rejected_event