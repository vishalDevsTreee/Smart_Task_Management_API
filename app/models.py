from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float, text, Numeric
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, nullable=False)
    name =Column(String, nullable=False)
    email =Column(String, nullable=False)
    password =Column(String, nullable=False)
    