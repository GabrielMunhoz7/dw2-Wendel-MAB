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
    period = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    material = Column(String(100), nullable=False)
    denomination = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    description = Column(Text, default="")
    historia = Column(Text, default="")
    contexto = Column(Text, default="")
    referencia = Column(String(500), default="")
    image_front = Column(String(500), default="")
    image_back = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())