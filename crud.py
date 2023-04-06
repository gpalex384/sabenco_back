import models
from sqlalchemy.orm import Session, joinedload

# Read all the events that belong to a given category whose start date is between two dates
def get_event_by_category(db: Session, startdate: str, enddate:str, category:str):
    return db.query(models.Event).filter(models.Event.startdate >= startdate,
                                         models.Event.startdate <= enddate,
                                         models.EventCategory.category_id == category).all()