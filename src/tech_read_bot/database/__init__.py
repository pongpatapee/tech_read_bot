from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Reading, Note
import os

class TechReadDao:
    def __init__(self, db_url=None):
        if db_url is None:
            db_url = os.getenv("READBOT_DB_URL", "sqlite:///readbot.db")
        self.engine = create_engine(db_url, echo=False, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.init_db()

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def create_reading(self, title, duration, status="in_progress"):
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