import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Note, Reading, Reminder


class TechReadDao:
    def __init__(self, db_url=None):
        if db_url is None:
            db_url = os.getenv("READBOT_DB_URL", "sqlite:///readbot.db")
        self.engine = create_engine(db_url, echo=False, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.init_db()

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def create_reading(self, title: str, duration: int, status: str = "in_progress"):
        with self.SessionLocal() as session:
            try:
                reading = Reading(title=title, duration=duration, status=status)
                session.add(reading)
                session.commit()
                session.refresh(reading)
                return reading
            except Exception as e:
                session.rollback()
                raise e

    def get_reading(self, id: int):
        with self.SessionLocal() as session:
            return session.query(Reading).filter(Reading.id == id).first()

    def get_readings(self, status: str = "in_progress"):
        with self.SessionLocal() as session:
            query = session.query(Reading)
            if status != "all":
                query = query.filter(Reading.status == status)

            return query.all()

    def update_reading(self, id: int, status: str):
        with self.SessionLocal() as session:
            try:
                reading = session.query(Reading).filter(Reading.id == id).first()

                if not reading:
                    raise Exception(f"Reading with id {id} not found")

                reading.status = status
                session.commit()
                session.refresh(reading)
                return reading

            except Exception as e:
                session.rollback()
                raise e

    def delete_reading(self, id: int):
        with self.SessionLocal() as session:
            try:
                reading = session.query(Reading).filter(Reading.id == id).first()

                if not reading:
                    raise Exception(f"Reading with id {id} not found")

                session.delete(reading)
                session.commit()

            except Exception as e:
                session.rollback()
                raise e

    def create_reminder(self, reading_id: int, reminder_datetime: datetime):
        with self.SessionLocal() as session:
            try:
                reminder = Reminder(
                    reading_id=reading_id, reminder_datetime=reminder_datetime
                )
                session.add(reminder)
                session.commit()
                session.refresh(reminder)
                return reminder
            except Exception as e:
                session.rollback()
                raise e

    def get_reminders(self):
        with self.SessionLocal() as session:
            return session.query(Reminder).all()

    def delete_reminder(self, id: int):
        with self.SessionLocal() as session:
            try:
                reminder = session.query(Reminder).filter(Reminder.id == id).first()

                if not reminder:
                    raise Exception(f"Reminder with id {id} not found")

                session.delete(reminder)
                session.commit()

            except Exception as e:
                session.rollback()
                raise e

    def create_note(self, reading_id, user_id, content):
        with self.SessionLocal() as session:
            try:
                note = Note(reading_id=reading_id, user_id=user_id, content=content)
                session.add(note)
                session.commit()
                session.refresh(note)
                return note
            except Exception as e:
                session.rollback()
                raise e
