import sqlalchemy.orm as orm
from database import database
from sqlalchemy import Column, Integer, String, ForeignKey


class TagModel(database.Model):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), unique=False, nullable=False)
    store = orm.relationship("StoreModel", back_populates="tags")
    items = orm.relationship("ItemModel", back_populates="tags", secondary="items_tags")
