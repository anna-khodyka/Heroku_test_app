'''описывает струкруктуру БД '''
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USERNAME = os.environ.get("DB_USERNAME", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "1234")
DATA_BASE = os.environ.get("DATA_BASE", "khodyka_db")

engine = create_engine(
    "postgresql+psycopg2://"+DB_USERNAME+":"+DB_PASSWORD+"@"+DB_HOST + "/" + DATA_BASE, echo=True
)

DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()


class Record(Base):
    '''описывает таблицу Record для хранения контактов'''
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    address = Column(String)
    email = Column(String)
    tags = Column(String)

    phones = relationship(
        "Phone", back_populates="record", cascade="all, delete, delete-orphan"
    )


class Phone(Base):
    '''описывает таблицу Phone для хранения телефонов'''
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    phone_value = Column(String, nullable=False)
    record_id = Column(Integer, ForeignKey("records.id"))

    record = relationship("Record", back_populates="phones")


class Note(Base):
    '''описывает таблицу notes для хранения заметок'''
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    note_tags = Column(String)
    note_text = Column(String)
    created_at = Column(Date)


# перенесла в get_db
# Base.metadata.bind = engine
# Base.metadata.create_all(engine)
