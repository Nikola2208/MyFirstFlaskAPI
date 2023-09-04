import sqlalchemy.orm as orm
from database import database
from sqlalchemy import Column, Integer, String


class StoreModel(database.Model):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    items = orm.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = orm.relationship("TagModel", back_populates="store", lazy="dynamic", cascade="all, delete")
