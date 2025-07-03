"""
Database module for managing reading data, notes, and reminders using SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime,  timezone
import os

Base = declarative_base()


class Reading(Base):
    __tablename__ = 'readings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    status = Column(Enum("done", "in_progress", name="status_enum"), default="in_progress", nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    duration = Column(Integer, nullable=False)

    # Relationships
    notes = relationship("Note", back_populates="reading", cascade="all, delete-orphan")



class Note(Base):
    """Model for reading notes."""
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    reading_id = Column(Integer, ForeignKey('readings.id'), nullable=False)
    user_id = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # Relationships
    reading = relationship("Reading", back_populates="notes")

