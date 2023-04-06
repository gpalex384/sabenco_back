from sqlalchemy import Column, Date, ForeignKey, String
from database import Base
from sqlalchemy.orm import relationship

class EventCategory(Base):
    __tablename__="eventcategory"
    event_id = Column(ForeignKey("event.id"), primary_key=True, index=True)
    category_id = Column(ForeignKey("category.id"), primary_key=True, index=True)

    event = relationship("Event", back_populates="categories")
    category = relationship("Category", back_populates="events")

class Event(Base):
    __tablename__="event"
    id= Column(String, primary_key=True, index=True)
    title = Column(String)
    detail = Column(String)
    startdate = Column(Date)
    enddate = Column(Date)
    category_id = Column(ForeignKey("category.id"))
    created = Column(Date)
    updated = Column(Date)

    categories = relationship("EventCategory", back_populates="event")

class Category(Base):
    __tablename__="category"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    categorytype_id = Column(ForeignKey("categorytype.id"))
    created = Column(Date)
    updated = Column(Date)

    events = relationship("EventCategory", back_populates="category")
    categorytype = relationship("CategoryType", back_populates="categories")

class CategoryType(Base):
    __tablename__="categorytype"
    id = Column(String, primary_key=True, index=True)
    type = Column(String)

    categories = relationship("Category", back_populates="categorytype")
