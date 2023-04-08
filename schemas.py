from datetime import date
from typing import List
from pydantic import Field, BaseModel
from pydantic.schema import Any, Union
from pydantic.utils import GetterDict

class UserBase(BaseModel):
    password: str

class User(UserBase):
    id: str
    username: Union[str,None]
    usermail: str
    role_id: str
    
    class Config:
            orm_mode = True

class Role(BaseModel):
    id: str
    name: str

    users: List[User] = []

    class Config:
        orm_mode = True


class EventCategoryGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in {'id', 'name', 'description','categorytype_id','created','updated'}:
            return getattr(self._obj.category, key)
        else:
            return super(EventCategoryGetter, self).get(key, default)
        
class EventCategory(BaseModel):
    id: str = Field(alias='id')
    name: str
    description: Union[str,None]
    categorytype_id: str
    created: date
    updated: date
    
    class Config:
        orm_mode = True
        getter_dict = EventCategoryGetter

class EventBase(BaseModel):
    title: str
    detail: Union[str,None]
    startdate: date
    enddate: Union[date,None]
    
    class Config:
        orm_mode = True

class Event(EventBase):
    id: str = Field(alias='id')
    created: date
    updated: date

    categories: List[EventCategory]
    
    class Config:
        orm_mode = True

class CategoryEventGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in {'id', 'title', 'detail','startdate','enddate', 'created', 'updated'}:
            return getattr(self._obj.event, key)
        else:
            return super(CategoryEventGetter, self).get(key, default)


class CategoryEvent(BaseModel):
    id: str = Field(alias='id')
    title: str
    detail: Union[str,None]
    startdate: date
    enddate: Union[date,None]
    created: date
    updated: date
    
    class Config:
        getter_dict = CategoryEventGetter
        orm_mode = True
    

class Category(BaseModel):
    id: str = Field(alias='id')
    name: str
    description: Union[str,None]
    categorytype_id: str
    created: date
    updated: date
    
    events: List[CategoryEvent]
    
    class Config:
        orm_mode = True

class CategoryType(BaseModel):
    id: str
    type: str
    created: date
    updated: date

    categories: List[Category] = []

    class Config:
        orm_mode = True