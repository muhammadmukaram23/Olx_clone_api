from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import models
import schemas
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        profile_picture=user.profile_picture
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Location CRUD operations
def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.location_id == location_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

def update_location(db: Session, location_id: int, location_update: schemas.LocationUpdate):
    db_location = db.query(models.Location).filter(models.Location.location_id == location_id).first()
    if db_location:
        update_data = location_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_location, field, value)
        db.commit()
        db.refresh(db_location)
    return db_location

def delete_location(db: Session, location_id: int):
    db_location = db.query(models.Location).filter(models.Location.location_id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location

# Category CRUD operations
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.category_id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_parent_categories(db: Session):
    return db.query(models.Category).filter(models.Category.parent_id.is_(None)).all()

def get_subcategories(db: Session, parent_id: int):
    return db.query(models.Category).filter(models.Category.parent_id == parent_id).all()

def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate):
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if db_category:
        update_data = category_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# Ad CRUD operations
def create_ad(db: Session, ad: schemas.AdCreate):
    db_ad = models.Ad(**ad.dict())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def get_ad(db: Session, ad_id: int):
    return db.query(models.Ad).filter(models.Ad.ad_id == ad_id).first()

def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).offset(skip).limit(limit).all()

def get_ads_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter(models.Ad.user_id == user_id).offset(skip).limit(limit).all()

def get_ads_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter(models.Ad.category_id == category_id).offset(skip).limit(limit).all()

def get_ads_by_location(db: Session, location_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter(models.Ad.location_id == location_id).offset(skip).limit(limit).all()

def search_ads(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter(
        or_(
            models.Ad.title.contains(query),
            models.Ad.description.contains(query)
        )
    ).offset(skip).limit(limit).all()

def update_ad(db: Session, ad_id: int, ad_update: schemas.AdUpdate):
    db_ad = db.query(models.Ad).filter(models.Ad.ad_id == ad_id).first()
    if db_ad:
        update_data = ad_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ad, field, value)
        db.commit()
        db.refresh(db_ad)
    return db_ad

def delete_ad(db: Session, ad_id: int):
    db_ad = db.query(models.Ad).filter(models.Ad.ad_id == ad_id).first()
    if db_ad:
        db.delete(db_ad)
        db.commit()
    return db_ad

# Ad Image CRUD operations
def create_ad_image(db: Session, ad_image: schemas.AdImageCreate):
    db_ad_image = models.AdImage(**ad_image.dict())
    db.add(db_ad_image)
    db.commit()
    db.refresh(db_ad_image)
    return db_ad_image

def get_ad_images(db: Session, ad_id: int):
    return db.query(models.AdImage).filter(models.AdImage.ad_id == ad_id).all()

def delete_ad_image(db: Session, image_id: int):
    db_image = db.query(models.AdImage).filter(models.AdImage.image_id == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
    return db_image

# Favorite CRUD operations
def create_favorite(db: Session, favorite: schemas.FavoriteCreate):
    db_favorite = models.Favorite(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).offset(skip).limit(limit).all()

def delete_favorite(db: Session, user_id: int, ad_id: int):
    db_favorite = db.query(models.Favorite).filter(
        and_(models.Favorite.user_id == user_id, models.Favorite.ad_id == ad_id)
    ).first()
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return db_favorite

def is_favorite(db: Session, user_id: int, ad_id: int):
    return db.query(models.Favorite).filter(
        and_(models.Favorite.user_id == user_id, models.Favorite.ad_id == ad_id)
    ).first() is not None

# Message CRUD operations
def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_for_ad(db: Session, ad_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(models.Message.ad_id == ad_id).offset(skip).limit(limit).all()

def get_conversation(db: Session, user1_id: int, user2_id: int, ad_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(
        and_(
            models.Message.ad_id == ad_id,
            or_(
                and_(models.Message.sender_id == user1_id, models.Message.receiver_id == user2_id),
                and_(models.Message.sender_id == user2_id, models.Message.receiver_id == user1_id)
            )
        )
    ).order_by(models.Message.sent_at).offset(skip).limit(limit).all()

def get_user_messages(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(
        or_(models.Message.sender_id == user_id, models.Message.receiver_id == user_id)
    ).offset(skip).limit(limit).all()

def update_message(db: Session, message_id: int, message_update: schemas.MessageUpdate):
    db_message = db.query(models.Message).filter(models.Message.message_id == message_id).first()
    if db_message:
        update_data = message_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_message, field, value)
        db.commit()
        db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int):
    db_message = db.query(models.Message).filter(models.Message.message_id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message

# Report CRUD operations
def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Report).offset(skip).limit(limit).all()

def get_reports_for_ad(db: Session, ad_id: int):
    return db.query(models.Report).filter(models.Report.ad_id == ad_id).all()

def delete_report(db: Session, report_id: int):
    db_report = db.query(models.Report).filter(models.Report.report_id == report_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
    return db_report

# Transaction CRUD operations
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

def get_user_transactions_as_buyer(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.buyer_id == user_id).offset(skip).limit(limit).all()

def get_user_transactions_as_seller(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.seller_id == user_id).offset(skip).limit(limit).all()

def update_transaction(db: Session, transaction_id: int, transaction_update: schemas.TransactionUpdate):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()
    if db_transaction:
        update_data = transaction_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_transaction, field, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction 