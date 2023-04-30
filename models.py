from sqlalchemy import Boolean, Column, Date, ForeignKey, String, text
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="user"
    id= Column(String, primary_key=True, index=True)
    username=Column(String, unique=True)
    usermail=Column(String, unique=True)
    password=Column(String)
    role_id=Column(ForeignKey("role.id"))
    created = Column(Date)
    updated = Column(Date)
    createdby = Column(String)
    updatedby = Column(String)

    role=relationship("Role", back_populates="users")

class Role(Base):
    __tablename__="role"
    id=Column(String, primary_key=True, index=True)
    name=Column(String, unique=True)
    created = Column(Date)
    updated = Column(Date)
    createdby = Column(String)
    updatedby = Column(String)

    users=relationship("User", back_populates="role")
    categories=relationship("CategoryRole", back_populates="role")

class EventCategory(Base):
    __tablename__="eventcategory"
    event_id = Column(ForeignKey("event.id"), primary_key=True, index=True)
    category_id = Column(ForeignKey("category.id"), primary_key=True, index=True)
    created = Column(Date)
    updated = Column(Date)
    createdby = Column(String)
    updatedby = Column(String)

    event = relationship("Event", back_populates="categories")
    category = relationship("Category", back_populates="events")


class Event(Base):
    __tablename__="event"
    id= Column(String, primary_key=True, index=True, default=text('uuid()'))
    title = Column(String)
    detail = Column(String)
    startdate = Column(Date)
    enddate = Column(Date)
    category_id = Column(ForeignKey("category.id"))
    created = Column(Date)
    updated = Column(Date)
    createdby = Column(String)
    updatedby = Column(String)
    published = Column(Boolean)

    categories = relationship("EventCategory", back_populates="event")
    eventdrafts = relationship("EventDraft", back_populates="event")


class EventDraft(Base):
    __tablename__="eventdraft"
    id= Column(String, primary_key=True, index=True, default=text('uuid()'))
    title = Column(String)
    detail = Column(String)
    startdate = Column(Date)
    enddate = Column(Date)
    created = Column(Date)
    updated = Column(Date)
    createdby = Column(String)
    updatedby = Column(String)
    pub_requested = Column(Boolean, default=0)
    moderator_comment = Column(String)
    published = Column(Boolean, default=0)
    publishdate = Column(Date)
    obsolete = Column(Boolean, default=0)
    event_id = Column(ForeignKey("event.id"))
  
    event = relationship("Event", back_populates="eventdrafts")
    

class Category(Base):
    __tablename__="category"
    id = Column(String, primary_key=True, index=True, default=text('uuid()'))
    name = Column(String)
    description = Column(String)
    created = Column(Date)
    updated = Column(Date)
    createdby = Column(String)
    updatedby = Column(String)
    active = Column(Boolean)

    events = relationship("EventCategory", back_populates="category")
    roles = relationship("CategoryRole", back_populates="category")

class CategoryRole(Base):
    __tablename__="categoryrole"
    role_id = Column(ForeignKey("role.id"), primary_key=True, index=True)
    category_id = Column(ForeignKey("category.id"), primary_key=True, index=True)
    created = Column(Date)
    updated = Column(Date)
    createdby = Column(String)
    updatedby = Column(String)

    role = relationship("Role", back_populates="categories")
    category = relationship("Category", back_populates="roles")


