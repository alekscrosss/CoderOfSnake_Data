from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from src.db.models import Role

class VehicleBase(BaseModel):
    license_plate: str

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int

    class Config:
        orm_mode = True

class ParkingRateBase(BaseModel):
    rate_per_hour: float
    rate_per_min: float
    rate_per_day: float
    rate_per_mon: float

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

from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional
from src.db.models import Role

class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr



