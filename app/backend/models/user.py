from slugify import slugify
from sqlalchemy import Column, Integer, String
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship
from sqlalchemy.sql.ddl import CreateTable

from app.backend.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship('Task', back_populates='user')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug:
            self.slug = slugify(self.username)


print(CreateTable(User.__table__))


@listens_for(User, 'before_insert')
def before_insert(_, __, target):
    if not target.slug:
        target.slug = slugify(target.username)


@listens_for(User, 'before_update')
def before_update(_, __, target):
    if not target.slug:
        target.slug = slugify(target.username)
