import sqlalchemy.orm as orm
from database import database
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class ItemModel(database.Model):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float(precision=2), unique=False, nullable=False)
    description = Column(String(100), unique=False, nullable=True)
    store_id = Column(Integer, ForeignKey("stores.id"), unique=False, nullable=False)
    store = orm.relationship("StoreModel", back_populates="items")
    tags = orm.relationship("TagModel", back_populates="items", secondary="items_tags")
