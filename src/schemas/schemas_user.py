from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from src.db.models import Role

class PlateBase(BaseModel):
    number: str

class PlateCreate(PlateBase):
    pass

class Plate(PlateBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class ParkingRateBase(BaseModel):
    amount: float
    duration: int

class ParkingRateCreate(ParkingRateBase):
    pass

class ParkingRate(ParkingRateBase):
    id: int

    class Config:
        from_attributes = True

class BlacklistBase(BaseModel):
    plate_id: int

class BlacklistCreate(BlacklistBase):
    pass

class Blacklist(BlacklistBase):
    id: int

    class Config:
        from_attributes = True

class ParkingHistoryBase(BaseModel):
    start_time: datetime
    end_time: datetime
    amount_paid: float

class ParkingHistoryCreate(ParkingHistoryBase):
    pass

class ParkingHistory(ParkingHistoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True

class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6, max_length=150)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Role

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


