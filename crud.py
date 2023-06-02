import datetime

from fastapi import HTTPException
import models, schemas
from sqlalchemy.orm import Session
from utils.utils import Utils
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, userdata: schemas.UserPass):
    try:
        db_user = models.User(**userdata.dict())
        db_user.created = datetime.datetime.now()
        db_user.updated = datetime.datetime.now()
        db_user.role_id = get_role_by_name(db, "visitor").id
        db_user.active = True
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except RuntimeError:
        raise HTTPException(status_code=400, detail="Incorrect user data") 
    return db_user

# Read all the events that belong to a given category whose start date is between two dates
def get_event_by_category(db: Session, startdate: str, enddate:str, category_id:str):
    return db.query(models.Event).filter(models.Event.startdate >= startdate,
                                         models.Event.startdate <= enddate,
                                         models.Event.id == models.EventCategory.event_id,
                                         models.EventCategory.category_id == category_id).all()

def get_related_events_by_event_id(db: Session, event_id: str):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    return Utils.get_related_events(db, db_event.id)

# Create an event given the title, detail, start date and end date
def create_eventdraft(db: Session, eventdata: schemas.EventDraftBase, user_id: str, event_id: str):
    try:
        db_eventdraft = models.EventDraft(**eventdata.dict())
        db_eventdraft.event_id = event_id
        db_eventdraft.createdby = user_id
        db_eventdraft.updatedby = user_id
        db.add(db_eventdraft)
        db.commit()
        db.refresh(db_eventdraft)
    except:
        raise HTTPException(status_code=401, detail="Incorrect event data")
    return db_eventdraft

def create_category(db: Session, categorydata: schemas.CategoryBase, user_id: str):
    try:
        db_category = models.Category(**categorydata.dict())
        db_category.createdby = user_id
        db_category.updatedby = user_id
        db_category.active = True
        db.add(db_category)
        db.commit()
        db.refresh(db_category)      
    except:
        raise HTTPException(status_code=400, detail="Category already exists")
    return db_category

def edit_category(db: Session, categorydata: schemas.CategoryBase, user_id: str, category_id: str):
    db_category = get_category_by_id(db, category_id)
    db_category.updated = datetime.datetime.now()
    db_category.updatedby = user_id
    db_category.name = categorydata.name
    db_category.description = categorydata.description
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: str):
    # Delete eventcategory links
    db_eventcategory_list = get_eventcategory_by_category_id(db, category_id)
    for db_eventcategory in db_eventcategory_list:
        db.delete(db_eventcategory)
        db.commit()
    # Delete category
    db_category = get_category_by_id(db, category_id)
    db_category_name = db_category.name
    db.delete(db_category)
    db.commit()
    return db_category_name

def assign_category_to_event(db: Session, db_event: models.Event, db_category: models.Category, user_id: str):
    db_eventcategory = models.EventCategory()
    db_eventcategory.category_id = db_category.id
    db_eventcategory.event_id = db_event.id
    db_eventcategory.createdby = user_id
    db_eventcategory.updatedby = user_id
    db.add(db_eventcategory)
    db.commit()

def link_events(db: Session, db_event_1: models.Event, db_event_2: models.Event, user_id: str, description: str):
    db_eventlink = models.EventLink()
    db_eventlink.event1_id = db_event_1.id
    db_eventlink.event2_id = db_event_2.id
    db_eventlink.link_description = description
    db_eventlink.createdby = user_id
    db_eventlink.updatedby = user_id
    db.add(db_eventlink)
    db.commit()

def assign_category_to_role(db: Session, db_role: models.Role, db_category: models.Category, user_id: str):
    db_categoryrole = models.CategoryRole()
    db_categoryrole.category_id = db_category.id
    db_categoryrole.role_id = db_role.id
    db_categoryrole.createdby = user_id
    db_categoryrole.updatedby = user_id
    db_categoryrole.created = datetime.datetime.now()
    db_categoryrole.updated = datetime.datetime.now()
    db.add(db_categoryrole)
    db.commit()

def assign_role_to_user(db: Session, role_id: str, db_user: models.User, user_id: str):
    db_user.role_id = role_id
    db_user.updated = datetime.datetime.now()
    db_user.updatedby = user_id
    db.add(db_user)
    db.commit()

# Edit an event draft given the title, detail, start date, end date and publication requested
def edit_eventdraft(db: Session, eventdata: schemas.EventDraftBase, user_id: str, db_eventdraft: models.EventDraft):
    eventdraft_data = eventdata.dict()
    db_eventdraft.updatedby = user_id
    db_eventdraft.updated = datetime.datetime.now()
    db_eventdraft.title = eventdraft_data.get('title')
    db_eventdraft.detail = eventdraft_data.get('detail')
    db_eventdraft.startdate = eventdraft_data.get('startdate')
    db_eventdraft.enddate = eventdraft_data.get('enddate')
    db_eventdraft.pub_requested = eventdraft_data.get('pub_requested')
    db.add(db_eventdraft)
    db.commit()
    db.refresh(db_eventdraft)
    return db_eventdraft

def get_event_by_id(db: Session, event_id: str):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

# Get the user data given the userId
def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Get the user data given the username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Get the user data given the usermail
def get_user_by_usermail(db: Session, usermail: str):
    return db.query(models.User).filter(models.User.usermail == usermail).first()

# Get the user role data given the userId
def get_user_role_by_id(db: Session, user_id: str, role: str):
    user_role_id = db.query(models.Role).filter(models.Role.name == role).first().id
    return db.query(models.User).filter(models.User.id == user_id,
                                        models.User.role_id == user_role_id).first()

def get_category_by_id(db: Session, category_id: str):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_eventcategory_by_category_id(db: Session, category_id: str):
    return db.query(models.EventCategory).filter(models.EventCategory.category_id == category_id).all()

# Publishes an event draft into an event
def publish_eventdraft(db: Session, eventdraft:str, user_id:str):
    # Update eventdraft
    db_eventdraft = get_eventdraft_by_id(db, eventdraft_id=eventdraft)
    db_eventdraft.published = True
    db_eventdraft.pub_requested = False
    db_eventdraft.publishdate = datetime.datetime.now()
    db_eventdraft.updated = datetime.datetime.now()
    db_eventdraft.updatedby = user_id
    db.add(db_eventdraft)
    db.commit()
    db.refresh(db_eventdraft)
    # Create event from eventdraft
    db_event = Utils.create_event_from_eventdraft(db, db_eventdraft)
    
    return db_event

def publish_unpublish_event(db: Session, db_event: models.Event, user_id: str, publish: bool):
    # Unpublish event
    db_event.published = publish
    db_event.updated = datetime.datetime.now()
    db_event.updatedby = user_id
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event

# Publishes an event draft into an event
def reject_eventdraft(db: Session, db_eventdraft:models.EventDraft, user_id:str, comment:str):
    # Update eventdraft
    db_eventdraft.moderator_comment = comment
    db_eventdraft.updated = datetime.datetime.now()
    db_eventdraft.updatedby = user_id
    db_eventdraft.pub_requested = False
    db.add(db_eventdraft)
    db.commit()
    db.refresh(db_eventdraft)
    
    return db_eventdraft

# Get the event draft data given the eventdraft_id
def get_eventdraft_by_id(db: Session, eventdraft_id: str):
    return db.query(models.EventDraft).filter(models.EventDraft.id == eventdraft_id).first()

# Get all the event drafts whose publication is requested
def get_eventdraft(db: Session):
    return db.query(models.EventDraft).filter(models.EventDraft.pub_requested == 1,
                                              models.EventDraft.obsolete == 0,
                                              models.EventDraft.published == 0).all()

# Get the event data given the event_id
def get_event_by_id(db: Session, event_id: str):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_eventdraft_by_user_id(db: Session, user_id: str):
    return db.query(models.EventDraft).filter(models.EventDraft.createdby == user_id).all()

def get_eventdrafts_by_event(db: Session, event_id: str):
    return db.query(models.EventDraft).filter(models.EventDraft.event_id == event_id, 
                                              models.EventDraft.obsolete == False,
                                              models.EventDraft.published == True).all()

def get_role_by_id(db: Session, role_id: str):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_role_by_name(db: Session, rolename: str):
    return db.query(models.Role).filter(models.Role.name == rolename).first()

def get_related_event_ids(db: Session, event_id: str):
    rel_events_ids = []
    ev2_related_events = db.query(models.EventLink).filter(models.EventLink.event1_id == event_id)
    for relevent in ev2_related_events:
        rel_events_ids.append(relevent.event2_id)
    ev1_related_events = db.query(models.EventLink).filter(models.EventLink.event2_id == event_id)
    for relevent in ev1_related_events:
        rel_events_ids.append(relevent.event1_id)
    return rel_events_ids