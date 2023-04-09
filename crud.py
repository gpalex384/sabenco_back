import models, schemas
from sqlalchemy.orm import Session

# Read all the events that belong to a given category whose start date is between two dates
def get_event_by_category(db: Session, startdate: str, enddate:str, category:str):
    return db.query(models.Event).filter(models.Event.startdate >= startdate,
                                         models.Event.startdate <= enddate,
                                         models.EventCategory.category_id == category).all()

# Create an event given the title, detail, start date and end date
def create_event(db: Session, event: schemas.EventBase, user_id: str):
    db_event = models.EventDraft(**event.dict())
    db_event.createdby = user_id
    db_event.updatedby = user_id
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Get the user data given the userId
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()