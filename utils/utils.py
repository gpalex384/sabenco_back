import datetime
from sqlalchemy.orm import Session

import models, crud

class Utils:

    def getNone():
        return None
    
    # Update/create event
    def create_event_from_eventdraft(db: Session, db_eventdraft: models.EventDraft):
        # Case eventdraft is not linked to an event, it means it will be a new event
        if db_eventdraft.event_id is None:
            db_event = models.Event()
            db_event.createdby = db_eventdraft.createdby
        # Case eventdraft is linked to an event, it means the eventdraft is meant to edit an existing event
        else:
            db_event = crud.get_event_by_id(db, db_eventdraft.event_id)
            db_event.updated = datetime.datetime.now()
        db_event.updatedby = db_eventdraft.updatedby
        db_event.detail = db_eventdraft.detail
        db_event.title = db_eventdraft.title
        db_event.startdate = db_eventdraft.startdate
        db_event.enddate = db_eventdraft.enddate
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event