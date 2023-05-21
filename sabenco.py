import datetime
from typing import List, Union
from typing_extensions import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashlib

import crud, schemas, models
from database import SessionLocal

from utils.utils import Utils

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/oauth2/access")
async def access(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return {"token": token}

@app.post("/token")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    passbytes = bytes(form_data.password, 'utf-8')
    hashed_password = hashlib.sha1(passbytes)
    password_hex_dig = hashed_password.hexdigest()
    print("Introduced password: %s" % password_hex_dig)
    print("User password: %s" % user.password)
    if not password_hex_dig == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = crud.get_user_by_username(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
async def read_users_me(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    #Utils.validate_user_admin(db, current_user.id)
    return current_user


# Register new user
@app.post("/users/register", response_model= schemas.UserBase)
def register_new_user(userdata: schemas.UserPass, db: Session = Depends(get_db)):
    userdata.password = hashlib.sha1(bytes(userdata.password, 'utf-8')).hexdigest()
    db_user = crud.create_user(db, userdata)
    return db_user

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

# Get the events related to an event
@app.get("/event/{event_id}/linkedevents", response_model=List[schemas.Event])
def read_linked_events(event_id: str, db: Session = Depends(get_db)):
    Utils.validate_event(db, event_id)
    related_events = crud.get_related_events_by_event_id(db, event_id)
    return related_events

# Get the user data given the userId
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return Utils.validate_user(db, user_id)

# Get role by id
@app.get("/roles/{role_id}", response_model=schemas.Role)
def read_role(role_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return Utils.validate_role(db, role_id)

# Get category by id
@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return Utils.validate_category(db, category_id)

# Get event drafts created by user (not posted / pending moderation)
@app.get("/eventdrafts", response_model=List[schemas.EventDraft])
def read_event_drafts_by_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_eventdraft = crud.get_eventdraft_by_user_id(db, current_user.id)
    return db_eventdraft

# Get event drafts pending to publish/moderate
@app.get("/eventdraft", response_model=List[schemas.EventDraft])
def read_event_drafts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    Utils.validate_user_moderator(db, current_user.id)
    return crud.get_eventdraft(db)

# Create an event draft given the title, detail, start date, end date and publication requested
@app.post("/eventdraft/create", response_model = schemas.EventDraftBase)
def create_event_draft(eventdata:schemas.EventDraftBase, event_id: Union[str,None] = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    Utils.validate_user_editor(db, current_user.id)
    #event_id = eventdata.dict().get('event_id')
    if event_id:
        Utils.validate_event(db, event_id)        
    db_created_eventdraft = crud.create_eventdraft(db, eventdata, current_user.id, event_id)
    return db_created_eventdraft

# Edit an event draft given the title, detail, start date, end date and publication requested
@app.put("/eventdraft/{eventdraft_id}", response_model = schemas.EventDraft)
def edit_eventdraft(eventdata:schemas.EventDraftBase, eventdraft_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_editor(db, current_user.id)
    db_eventdraft = Utils.validate_eventdraft(db, eventdraft_id)
    db_edited_eventdraft = crud.edit_eventdraft(db, eventdata, current_user.id, db_eventdraft)
    return db_edited_eventdraft

# Accept an event draft, making it become a published event
@app.post("/eventdraft/{eventdraft_id}/publish", response_model = schemas.Event)
def publish_eventdraft(eventdraft_id: str, user_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_eventdraft(db, eventdraft_id)
    Utils.validate_user_moderator(db, user_id)
    # Publish eventdraft
    db_published_event = crud.publish_eventdraft(db, eventdraft_id, user_id)
    return db_published_event

# Reject an event draft, adding a comment from the moderator
@app.put("/eventdraft/{eventdraft_id}/reject", response_model = schemas.EventDraft)
def reject_eventdraft(comment: str, eventdraft_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_comment(db, comment)
    Utils.validate_user_moderator(db, current_user.id)
    db_eventdraft = Utils.validate_eventdraft(db, eventdraft_id)
    # Edit eventdraft
    db_rejected_eventdraft = crud.reject_eventdraft(db, db_eventdraft, current_user.id, comment)
    return db_rejected_eventdraft

# Unpublish an event
@app.put("/event/{event_id}/unpublish", response_model = schemas.Event)
def unpublish_event(event_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    db_event = Utils.validate_event(db, event_id)
    # Unpublish event
    db_unpublished_event = crud.publish_unpublish_event(db, db_event, current_user.id, False)
    return db_unpublished_event

# Publish an existing unpublished event
@app.put("/event/{event_id}/publish", response_model = schemas.Event)
def publish_event(event_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    db_event = Utils.validate_event(db, event_id)
    # Publish event
    db_published_event = crud.publish_unpublish_event(db, db_event, current_user.id, True)
    return db_published_event

# Assign category to an event
@app.post("/event/{event_id}/category/{category_id}")
def assign_category_to_event(event_id: str, category_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    db_event = Utils.validate_event(db, event_id)
    db_category = Utils.validate_category(db, category_id)
    # Assign category to event
    crud.assign_category_to_event(db, db_event, db_category, current_user.id)
    return {"ok": "The event '%s' has been classified in the category '%s'" % (db_event.title,db_category.name)}

# Link two events
@app.post("/eventlink/{event_id_1}/{event_id_2}")
def link_two_events(event_id_1: str, event_id_2: str, description: Union[None,str] = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    db_event_1 = Utils.validate_event(db, event_id_1)
    db_event_2 = Utils.validate_event(db, event_id_2)
    # Link events
    crud.link_events(db, db_event_1, db_event_2, current_user.id, description)
    return {"ok": "The events '%s' and '%s' have been linked" % (db_event_1.title,db_event_2.title)}

# Assign category to role
@app.post("/category/{category_id}/role/{role_id}")
def assign_category_to_role(role_id: str, category_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    db_role = Utils.validate_role(db, role_id)
    db_category = Utils.validate_category(db, category_id)
    # Assign category to event
    crud.assign_category_to_role(db, db_role, db_category, current_user.id)
    return {"ok": "The category '%s' has been linked to the role '%s'" % (db_category.name,db_role.name)}

# Assign role to user
@app.post("/users/{user_id}/role/{role_id}")
def assign_role_to_user(role_id: str, user_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    db_role = Utils.validate_role(db, role_id)
    db_user = Utils.validate_user(db, user_id)
    # Assign category to event
    crud.assign_role_to_user(db, db_role.id, db_user, current_user.id)
    return {"ok": "The user '%s' has been linked to the role '%s'" % (db_user.username,db_role.name)}

# Create category
@app.post("/category/create", response_model= schemas.Category)
def create_category(categorydata: schemas.CategoryBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    # Create category
    db_category = crud.create_category(db, categorydata, current_user.id)
    return db_category

# Edit category
@app.put("/category/{category_id}/update", response_model= schemas.Category)
def edit_category(category_id: str, categorydata: schemas.CategoryBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    Utils.validate_category(db, category_id)
    # Update category
    db_category = crud.edit_category(db, categorydata, current_user.id, category_id)
    return db_category

# Delete category
@app.delete("/category/{category_id}/delete")
def delete_category(category_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Exception control
    Utils.validate_user_admin(db, current_user.id)
    Utils.validate_category(db, category_id)
    # Delete category
    deleted_category_name = crud.delete_category(db, category_id)
    return {"ok": "The category '" + deleted_category_name + "' has been deleted"}
