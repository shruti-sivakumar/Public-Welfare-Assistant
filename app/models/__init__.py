"""
SQLAlchemy models for the Data Interpreter Assistant
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Citizen(Base):
    """Citizens table model"""
    __tablename__ = "citizens"
    
    citizen_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Officer(Base):
    """Officers table model"""
    __tablename__ = "officers"
    
    officer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100))
    rank = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Scheme(Base):
    """Schemes table model"""
    __tablename__ = "schemes"
    
    scheme_id = Column(Integer, primary_key=True, index=True)
    scheme_name = Column(String(200), nullable=False)
    description = Column(Text)
    eligibility = Column(Text)
    benefits = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
