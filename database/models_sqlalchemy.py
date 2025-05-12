from enum import unique

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from database.database_sqlalchemy import Base


class User(Base):
    """
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120))
    fullname = Column(String(120))
    firstname = Column(String(120))
    lastname = Column(String(120))
    telegram_id = Column(Integer, unique=True)
    registration_date = Column(DateTime, default=datetime.utcnow)


class Groups(Base):
    """
    """
    __tablename__ = 'groups_list'

    id = Column(Integer, primary_key=True)
    username = Column(String(120))
    name = Column(String(120))


class Admins(Base):
    """
    """
    __tablename__ = 'admin_list'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)


class Vip(Base):
    """
    """
    __tablename__ = 'vip_panel'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String(120))
