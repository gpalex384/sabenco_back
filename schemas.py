from datetime import date
from typing import List
from pydantic import Field, BaseModel
from pydantic.schema import Any, Union
from pydantic.utils import GetterDict

class RoleGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in {'id','name','created','updated'}:
            return getattr(self._obj.role, key)
        else:
            return super(RoleGetter, self).get(key, default)
        
class CategoryGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in {'id', 'name', 'description','created','updated'}:
            return getattr(self._obj.category, key)
        else:
            return super(CategoryGetter, self).get(key, default)
        
class EventGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in {'id', 'title', 'detail','startdate','enddate', 'created', 'updated', 'published'}:
            return getattr(self._obj.event, key)
        else:
            return super(EventGetter, self).get(key, default)

class UserBase(BaseModel):
    username: str
    usermail: str
    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str
    class Config:
        orm_mode = True

class CategoryRole(BaseModel):
    id: str = Field(alias='id')
    name: str
    created: date
    updated: date
    class Config:
        orm_mode = True
        getter_dict = RoleGetter

class UserRole(BaseModel):
    id: str
    name: str
    created: date
    updated: date
    class Config:
        orm_mode = True
        getter_dict = RoleGetter

class CategoryBase(BaseModel):
    name: str
    description: Union[str,None]
    class Config:
        orm_mode = True

class RoleCategory(BaseModel):
    id: str = Field(alias='id')
    name: str
    description: Union[str,None]
    created: date
    updated: date
    class Config:
        orm_mode = True
        getter_dict = CategoryGetter
        
class EventCategory(BaseModel):
    id: str = Field(alias='id')
    name: str
    description: Union[str,None]
    created: date
    updated: date
    class Config:
        orm_mode = True
        getter_dict = CategoryGetter

class EventBase(BaseModel):
    title: str
    detail: str
    startdate: date
    enddate: Union[date,None] 
    class Config:
        orm_mode = True

class CategoryEvent(BaseModel):
    id: str = Field(alias='id')
    title: str
    detail: Union[str,None]
    startdate: date
    enddate: Union[date,None]
    created: date
    updated: date
    published: bool
    class Config:
        getter_dict = EventGetter
        orm_mode = True

class LinkEvent(BaseModel):
    id: str = Field(alias='id')
    title: str
    detail: Union[str,None]
    startdate: date
    enddate: Union[date,None]
    created: date
    updated: date
    published: bool
    class Config:
        getter_dict = EventGetter
        orm_mode = True

class EventDraftBase(EventBase):
    pub_requested: Union[int,None]
    class Config:
        orm_mode = True

class UserPass(UserBase):
    password: str
    class Config:
        orm_mode = True

class User(UserPass):
    id: str
    role_id: str
    created: date
    updated: date
    class Config:
        orm_mode = True

class Role(RoleBase):
    id: str
    created: date
    updated: date
    users: List[UserBase] = [] 
    categories: List[RoleCategory] = []
    class Config:
        orm_mode = True

class Event(EventBase):
    id: str = Field(alias='id')
    created: date
    updated: date
    published: bool
    categories: List[EventCategory] = []
    class Config:
        orm_mode = True

class EventDraft(EventDraftBase):
    id: str = Field(alias='id')
    event_id: Union[str,None]
    created: date
    updated: date
    moderator_comment: Union[str,None]
    published: bool
    publishdate: Union[date,None]
    obsolete: bool
    class Config:
        orm_mode = True

class Category(CategoryBase):
    id: str = Field(alias='id')
    created: date
    updated: date
    events: List[CategoryEvent] = []
    roles: List[CategoryRole] = []
    class Config:
        orm_mode = True

