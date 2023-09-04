from database import database
from sqlalchemy import Column, Integer, String
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class UserModel(database.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(), unique=False, nullable=False)
    role = Column(String(), unique=False, nullable=False)
