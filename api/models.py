from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Coin(Base):
    __tablename__ = "coins"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    country = Column(String(100), nullable=False)
    value = Column(String(50), nullable=False)
    rarity = Column(String(50), nullable=False)
    description = Column(Text, default="")
    image_url = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())