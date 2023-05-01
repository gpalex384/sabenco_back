import datetime
from typing import List
from fastapi import HTTPException
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
    
    def validate_user(db: Session, user_id: str):
        db_user = crud.get_user_by_id(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    
    def validate_useradmin(db: Session, user_id: str):
        db_useradmin = crud.get_useradmin_by_id(db, user_id)
        if db_useradmin is None:
            raise HTTPException(status_code=401, detail="User is not an administrator")
        return db_useradmin
        
    def validate_event(db: Session, event_id: str):
        db_event = crud.get_event_by_id(db, event_id)
        if db_event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return db_event
    
    def validate_role(db: Session, role_id: str):
        db_role = crud.get_role_by_id(db, role_id)
        if db_role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        return db_role
        
    def validate_eventdraft(db: Session, eventdraft_id: str):
        db_eventdraft = crud.get_eventdraft_by_id(db, eventdraft_id)
        if db_eventdraft is None:
            raise HTTPException(status_code=404, detail="Event draft not found")
        return db_eventdraft
        
    def validate_comment(db: Session, comment: str):
        if comment is None or comment == '':
            raise HTTPException(status_code=401, detail="The comment is required for rejecting")
        
    def validate_category(db: Session, category_id: str):
        db_category = crud.get_category_by_id(db, category_id=category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return db_category
    
    def get_related_events(db: Session, event_id: str):
        rel_events_ids = crud.get_related_event_ids(db, event_id)
        event_dicts = []
        for id in rel_events_ids:
            db_event = crud.get_event_by_id(db, id).__dict__
            event_dicts.append(db_event)
        return event_dicts
