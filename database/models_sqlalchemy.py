from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.database_sqlalchemy import Base

# from sqlalchemy.orm import declarative_base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), nullable=True)  # username может быть не у всех
    fullname = Column(String(120), nullable=False)  # обязательное поле
    firstname = Column(String(120), nullable=True)
    lastname = Column(String(120), nullable=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.fullname}, {self.firstname}, {self.lastname}, {self.telegram_id}, {self.registration_date}"


class Groups(Base):
    __tablename__ = 'groups_list'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    name = Column(String(120), nullable=False)

    def __repr__(self):
        return f"id={self.id}, name='{self.name}')"


class Admins(Base):
    __tablename__ = 'admin_list'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"id={self.id}, telegram_id={self.telegram_id}"


class Vip(Base):
    __tablename__ = 'vip_panel'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status_vip = Column(String(120), nullable=False)
    number_of_days = Column(Integer, nullable=False)
    name = Column(String(120), nullable=False)


    def __repr__(self):
        return f"id={self.id}, name={self.name}"
