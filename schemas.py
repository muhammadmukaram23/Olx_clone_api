from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

class ConditionEnum(str, Enum):
    NEW = "New"
    USED = "Used"

class TransactionStatusEnum(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# User Schemas
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    profile_picture: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Location Schemas
class LocationBase(BaseModel):
    city: str
    state: Optional[str] = None
    country: str = "Pakistan"

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class Location(LocationBase):
    location_id: int
    
    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None

class Category(CategoryBase):
    category_id: int
    
    class Config:
        from_attributes = True

# Ad Image Schemas
class AdImageBase(BaseModel):
    image_url: str

class AdImageCreate(AdImageBase):
    ad_id: int

class AdImage(AdImageBase):
    image_id: int
    ad_id: int
    
    class Config:
        from_attributes = True

# Ad Schemas
class AdBase(BaseModel):
    title: str
    description: str
    price: Decimal
    condition: ConditionEnum
    category_id: int
    location_id: Optional[int] = None

class AdCreate(AdBase):
    user_id: int

class AdUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    condition: Optional[ConditionEnum] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    is_sold: Optional[bool] = None

class Ad(AdBase):
    ad_id: int
    user_id: int
    is_sold: bool
    created_at: datetime
    updated_at: datetime
    user: Optional[User] = None
    category: Optional[Category] = None
    location: Optional[Location] = None
    images: List[AdImage] = []
    
    class Config:
        from_attributes = True

# Favorite Schemas
class FavoriteBase(BaseModel):
    user_id: int
    ad_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    user: Optional[User] = None
    ad: Optional[Ad] = None
    
    class Config:
        from_attributes = True

# Message Schemas
class MessageBase(BaseModel):
    message: str
    ad_id: int

class MessageCreate(MessageBase):
    sender_id: int
    receiver_id: int

class MessageUpdate(BaseModel):
    message: Optional[str] = None

class Message(MessageBase):
    message_id: int
    sender_id: int
    receiver_id: int
    sent_at: datetime
    sender: Optional[User] = None
    receiver: Optional[User] = None
    
    class Config:
        from_attributes = True

# Report Schemas
class ReportBase(BaseModel):
    reason: str

class ReportCreate(ReportBase):
    ad_id: int
    reported_by: int

class Report(ReportBase):
    report_id: int
    ad_id: int
    reported_by: int
    reported_at: datetime
    ad: Optional[Ad] = None
    reporter: Optional[User] = None
    
    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionBase(BaseModel):
    amount: Decimal

class TransactionCreate(TransactionBase):
    ad_id: int
    buyer_id: int
    seller_id: int

class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatusEnum] = None
    amount: Optional[Decimal] = None

class Transaction(TransactionBase):
    transaction_id: int
    ad_id: int
    buyer_id: int
    seller_id: int
    status: TransactionStatusEnum
    transaction_date: datetime
    ad: Optional[Ad] = None
    buyer: Optional[User] = None
    seller: Optional[User] = None
    
    class Config:
        from_attributes = True

# Response Models
class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone: Optional[str]
    profile_picture: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdResponse(BaseModel):
    ad_id: int
    title: str
    description: str
    price: Decimal
    condition: ConditionEnum
    is_sold: bool
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None
    category: Optional[Category] = None
    location: Optional[Location] = None
    images: List[AdImage] = []
    
    class Config:
        from_attributes = True 