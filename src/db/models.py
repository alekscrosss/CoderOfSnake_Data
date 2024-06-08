import os
import enum
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime, Boolean, Enum, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Role(enum.Enum):
    user = 'user'
    admin = 'admin'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
    status_ban = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    license_plate = Column(String(20), nullable=False, unique=True)
    parking_sessions = relationship("ParkingSession", back_populates="vehicle")
    registered_user = relationship("RegisteredUser", back_populates="vehicle", uselist=False)

class ParkingSession(Base):
    __tablename__ = "parking_sessions"

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    entry_time = Column(DateTime, nullable=False, default=func.now())
    exit_time = Column(DateTime)
    payment_status = Column(String(20), nullable=False, default='not paid')
    amount_due = Column(DECIMAL(10, 2))
    is_registered = Column(Boolean, default=False)

    vehicle = relationship("Vehicle", back_populates="parking_sessions")


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True)
    rate_per_hour = Column(DECIMAL(10, 2), nullable=False)
    rate_per_min = Column(DECIMAL(10, 2), nullable=False)
    rate_per_day = Column(DECIMAL(10, 2), nullable=False)
    rate_per_mon = Column(DECIMAL(10, 2), nullable=False)


class RegisteredUser(Base):
    __tablename__ = "registered_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    registration_date = Column(DateTime, nullable=False, default=func.now())
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False)

    user = relationship("User")
    vehicle = relationship("Vehicle", back_populates="registered_user")


Base.metadata.create_all(bind=engine)
