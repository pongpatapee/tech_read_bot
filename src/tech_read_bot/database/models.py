from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    status = Column(
        Enum("done", "in_progress", name="status_enum"),
        default="in_progress",
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    duration = Column(Integer, nullable=False)

    # Relationships
    notes = relationship("Note", back_populates="reading", cascade="all, delete-orphan")
    reminders = relationship(
        "Reminders", back_populates="reading", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"Reading(id={self.id}, title='{self.title}', status='{self.status}', created_at={self.created_at}, duration={self.duration})"


class Reminders(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    reading_id = Column(Integer, ForeignKey("readings.id"), nullable=False)
    reminder_datetime = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    reading = relationship("Reading", back_populates="reminders")


class Note(Base):
    """Model for reading notes."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    reading_id = Column(Integer, ForeignKey("readings.id"), nullable=False)
    user_id = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    reading = relationship("Reading", back_populates="notes")
