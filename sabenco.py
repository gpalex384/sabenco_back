import datetime
from typing import List, Union
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from database import SessionLocal

from utils.utils import Utils

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
@app.get("/event/{category_id}/{startdate}/{enddate}", response_model = List[schemas.Event])
def read_events_by_dates_and_category(category_id: str, startdate: str, enddate: str, db: Session = Depends(get_db)):
    try:
        datetime.date.fromisoformat(startdate)
        datetime.date.fromisoformat(enddate)
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect data format, should be YYYY-MM-DD")
    Utils.validate_category(db, category_id)
    db_event_by_category = crud.get_event_by_category(db, startdate, enddate, category_id)
    return db_event_by_category

# Get the user data given the userId
#TODO encrypt password 
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    return Utils.validate_user(db, user_id)

# Get role by id
@app.get("/roles/{role_id}", response_model=schemas.Role)
def read_role(role_id: str, db: Session = Depends(get_db)):
    return Utils.validate_role(db, role_id)

# Get category by id
@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: str, db: Session = Depends(get_db)):
    return Utils.validate_category(db, category_id)

# Get event drafts created by user (not posted / pending moderation)
@app.get("/users/{user_id}/eventdrafts", response_model=List[schemas.EventDraft])
def read_event_drafts_by_user(user_id: str, db: Session = Depends(get_db)):
    Utils.validate_user(db, user_id)
    db_eventdraft = crud.get_eventdraft_by_user_id(db, user_id)
    return db_eventdraft

# Create an event draft given the title, detail, start date, end date and publication requested
@app.post("/users/{user_id}/eventdraft", response_model = schemas.EventDraftBase)
def create_event_draft(eventdata:schemas.EventDraftBase, user_id: str, db: Session = Depends(get_db)):
    Utils.validate_user(db, user_id)
    event_id = eventdata.dict().get('event_id')
    if event_id:
        Utils.validate_event(db, event_id)        
    db_created_eventdraft = crud.create_eventdraft(db, eventdata, user_id, event_id)
    return db_created_eventdraft

# Create an event draft given the title, detail, start date, end date and publication requested
@app.put("/users/{user_id}/eventdraft/{eventdraft_id}", response_model = schemas.EventDraft)
def edit_eventdraft(eventdata:schemas.EventDraftBase, user_id: str, eventdraft_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    db_eventdraft = Utils.validate_eventdraft(db, eventdraft_id)
    db_edited_eventdraft = crud.edit_eventdraft(db, eventdata, user_id, db_eventdraft)
    return db_edited_eventdraft

# Accept an event draft, making it become a published event
@app.post("/users/{user_id}/eventdraft/{eventdraft_id}/publish", response_model = schemas.Event)
def publish_eventdraft(eventdraft_id: str, user_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    Utils.validate_eventdraft(db, eventdraft_id)
    # Publish eventdraft
    db_published_event = crud.publish_eventdraft(db, eventdraft_id, user_id)
    return db_published_event

# Reject an event draft, adding a comment from the moderator
@app.put("/users/{user_id}/eventdraft/{eventdraft_id}/reject", response_model = schemas.EventDraft)
def reject_eventdraft(comment: str, eventdraft_id: str, user_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_comment(db, comment)
    Utils.validate_user(db, user_id)
    db_eventdraft = Utils.validate_eventdraft(db, eventdraft_id)
    # Edit eventdraft
    db_rejected_eventdraft = crud.reject_eventdraft(db, db_eventdraft, user_id, comment)
    return db_rejected_eventdraft

# Unpublish an event
@app.put("/users/{user_id}/event/{event_id}/unpublish", response_model = schemas.Event)
def unpublish_event(event_id: str, user_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    db_event = Utils.validate_event(db, event_id)
    # Unpublish event
    db_unpublished_event = crud.publish_unpublish_event(db, db_event, user_id, False)
    return db_unpublished_event

@app.put("/users/{user_id}/event/{event_id}/publish", response_model = schemas.Event)
def publish_event(event_id: str, user_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    db_event = Utils.validate_event(db, event_id)
    # Publish event
    db_published_event = crud.publish_unpublish_event(db, db_event, user_id, True)
    return db_published_event

# Assign category to event
@app.post("/users/{user_id}/event/{event_id}/category/{category_id}")
def assign_category_to_event(event_id: str, user_id: str, category_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    Utils.validate_useradmin(db, user_id)
    db_event = Utils.validate_event(db, event_id)
    db_category = Utils.validate_category(db, category_id)
    # Assign category to event
    crud.assign_category_to_event(db, db_event, db_category, user_id)
    return {"ok": "The event '%s' has been classified in the category '%s'" % (db_event.title,db_category.name)}

# Assign category to role
@app.post("/users/{user_id}/category/{category_id}/role/{role_id}")
def assign_category_to_role(user_id: str, role_id: str, category_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    Utils.validate_useradmin(db, user_id)
    db_role = Utils.validate_role(db, role_id)
    db_category = Utils.validate_category(db, category_id)
    # Assign category to event
    crud.assign_category_to_role(db, db_role, db_category, user_id)
    return {"ok": "The category '%s' has been linked to the role '%s'" % (db_category.name,db_role.name)}

@app.post("/users/{user_id}/category/create", response_model= schemas.Category)
def create_category(user_id: str, categorydata: schemas.CategoryBase, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    Utils.validate_useradmin(db, user_id)
    # Create category
    db_category = crud.create_category(db, categorydata, user_id)
    return db_category

@app.put("/users/{user_id}/category/{category_id}/update", response_model= schemas.Category)
def edit_category(user_id: str, category_id: str, categorydata: schemas.CategoryBase, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    Utils.validate_useradmin(db, user_id)
    Utils.validate_category(db, category_id)
    # Update category
    db_category = crud.edit_category(db, categorydata, user_id, category_id)
    return db_category

@app.delete("/users/{user_id}/category/{category_id}/delete")
def delete_category(user_id: str, category_id: str, db: Session = Depends(get_db)):
    # Exception control
    Utils.validate_user(db, user_id)
    Utils.validate_useradmin(db, user_id)
    Utils.validate_category(db, category_id)
    # Delete category
    deleted_category_name = crud.delete_category(db, category_id)
    return {"ok": "The category '" + deleted_category_name + "' has been deleted"}
