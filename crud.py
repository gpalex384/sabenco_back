import models, schemas
from sqlalchemy.orm import Session

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

def get_event_by_id(db: Session, event_id: str):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

# Get the user data given the userId
def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_category_by_id(db: Session, category_id: str):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

# Publishes an event draft into an event
def publish_event(db: Session, eventdraft:models.EventDraft, user_id:str):
    db_eventdraft = eventdraft
    db_eventdraft.published = True
    db_eventdraft.updatedby = user_id
    db.add(db_eventdraft)
    db.commit()
    db.refresh(db_eventdraft)
    return db_eventdraft

# Get the event draft data given the eventdraft_id
def get_eventdraft_by_id(db: Session, eventdraft_id: str):
    return db.query(models.EventDraft).filter(models.EventDraft.id == eventdraft_id).first()

def get_eventdraft_by_user_id(db: Session, user_id: str):
    return db.query(models.EventDraft).filter(models.EventDraft.createdby == user_id).all()