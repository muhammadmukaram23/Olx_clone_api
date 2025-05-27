from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class ConditionEnum(enum.Enum):
    NEW = "New"
    USED = "Used"

class TransactionStatusEnum(enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    profile_picture = Column(String(255))
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    ads = relationship("Ad", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    favorites = relationship("Favorite", back_populates="user")
    reports = relationship("Report", back_populates="reporter")
    buyer_transactions = relationship("Transaction", foreign_keys="Transaction.buyer_id", back_populates="buyer")
    seller_transactions = relationship("Transaction", foreign_keys="Transaction.seller_id", back_populates="seller")

class Location(Base):
    __tablename__ = "locations"
    
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    country = Column(String(100), default="Pakistan")
    
    # Relationships
    ads = relationship("Ad", back_populates="location")

class Category(Base):
    __tablename__ = "categories"
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.category_id", ondelete="SET NULL"))
    
    # Relationships
    parent = relationship("Category", remote_side="Category.category_id")
    ads = relationship("Ad", back_populates="category")

class Ad(Base):
    __tablename__ = "ads"
    
    ad_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    condition = Column(Enum(ConditionEnum), nullable=False)
    is_sold = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User", back_populates="ads")
    category = relationship("Category", back_populates="ads")
    location = relationship("Location", back_populates="ads")
    images = relationship("AdImage", back_populates="ad")
    favorites = relationship("Favorite", back_populates="ad")
    messages = relationship("Message", back_populates="ad")
    reports = relationship("Report", back_populates="ad")
    transactions = relationship("Transaction", back_populates="ad")

class AdImage(Base):
    __tablename__ = "ad_images"
    
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey("ads.ad_id", ondelete="CASCADE"))
    image_url = Column(String(255))
    
    # Relationships
    ad = relationship("Ad", back_populates="images")

class Favorite(Base):
    __tablename__ = "favorites"
    
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    ad_id = Column(Integer, ForeignKey("ads.ad_id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    ad = relationship("Ad", back_populates="favorites")

class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    ad_id = Column(Integer, ForeignKey("ads.ad_id"), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    ad = relationship("Ad", back_populates="messages")

class Report(Base):
    __tablename__ = "reports"
    
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey("ads.ad_id"))
    reported_by = Column(Integer, ForeignKey("users.user_id"))
    reason = Column(Text)
    reported_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    ad = relationship("Ad", back_populates="reports")
    reporter = relationship("User", back_populates="reports")

class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey("ads.ad_id"))
    buyer_id = Column(Integer, ForeignKey("users.user_id"))
    seller_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(DECIMAL(10, 2))
    status = Column(Enum(TransactionStatusEnum), default=TransactionStatusEnum.PENDING)
    transaction_date = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    ad = relationship("Ad", back_populates="transactions")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="buyer_transactions")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="seller_transactions") 