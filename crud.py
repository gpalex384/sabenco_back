import datetime
import models, schemas
from sqlalchemy.orm import Session
from utils.utils import Utils

# Read all the events that belong to a given category whose start date is between two dates
def get_event_by_category(db: Session, startdate: str, enddate:str, category_id:str):
    return db.query(models.Event).filter(models.Event.startdate >= startdate,
                                         models.Event.startdate <= enddate,
                                         models.EventCategory.category_id == category_id).all()

# Create an event given the title, detail, start date and end date
def create_eventdraft(db: Session, eventdata: schemas.EventDraftBase, user_id: str, event_id: str):
    db_eventdraft = models.EventDraft(**eventdata.dict())
    db_eventdraft.event_id = event_id
    db_eventdraft.createdby = user_id
    db_eventdraft.updatedby = user_id
    db.add(db_eventdraft)
    db.commit()
    db.refresh(db_eventdraft)
    return db_eventdraft

def create_category(db: Session, categorydata: schemas.CategoryBase, user_id: str):
    db_category = models.Category(**categorydata.dict())
    db_category.createdby = user_id
    db_category.updatedby = user_id
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
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

# Get the user data given the userId
def get_useradmin_by_id(db: Session, user_id: str):
    admin_role_id = db.query(models.Role).filter(models.Role.name == 'admin').first().id
    return db.query(models.User).filter(models.User.id == user_id,
                                        models.User.role_id == admin_role_id).first()

def get_category_by_id(db: Session, category_id: str):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

# Publishes an event draft into an event
def publish_eventdraft(db: Session, eventdraft:str, user_id:str):
    # Update eventdraft
    db_eventdraft = get_eventdraft_by_id(db, eventdraft_id=eventdraft)
    db_eventdraft.published = True
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

# Get the event data given the event_id
def get_event_by_id(db: Session, event_id: str):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_eventdraft_by_user_id(db: Session, user_id: str):
    return db.query(models.EventDraft).filter(models.EventDraft.createdby == user_id).all()

def get_eventdrafts_by_event(db: Session, event_id: str):
    return db.query(models.EventDraft).filter(models.EventDraft.event_id == event_id, 
                                              models.EventDraft.obsolete == False,
                                              models.EventDraft.published == True).all()