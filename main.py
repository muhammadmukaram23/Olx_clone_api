from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
import models
import schemas
import crud

# Database configuration - credentials directly in main file
DATABASE_URL = "mysql+pymysql://root:@localhost/olx_clone"

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="OLX Clone API",
    description="A comprehensive API for OLX clone marketplace",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to OLX Clone API"}

# USER ENDPOINTS
@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.UserResponse], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# LOCATION ENDPOINTS
@app.post("/locations/", response_model=schemas.Location, tags=["Locations"])
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db=db, location=location)

@app.get("/locations/", response_model=List[schemas.Location], tags=["Locations"])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations

@app.get("/locations/{location_id}", response_model=schemas.Location, tags=["Locations"])
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@app.put("/locations/{location_id}", response_model=schemas.Location, tags=["Locations"])
def update_location(location_id: int, location_update: schemas.LocationUpdate, db: Session = Depends(get_db)):
    db_location = crud.update_location(db, location_id=location_id, location_update=location_update)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@app.delete("/locations/{location_id}", tags=["Locations"])
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.delete_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}

# CATEGORY ENDPOINTS
@app.post("/categories/", response_model=schemas.Category, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category], tags=["Categories"])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/parent", response_model=List[schemas.Category], tags=["Categories"])
def read_parent_categories(db: Session = Depends(get_db)):
    categories = crud.get_parent_categories(db)
    return categories

@app.get("/categories/{category_id}/subcategories", response_model=List[schemas.Category], tags=["Categories"])
def read_subcategories(category_id: int, db: Session = Depends(get_db)):
    categories = crud.get_subcategories(db, parent_id=category_id)
    return categories

@app.get("/categories/{category_id}", response_model=schemas.Category, tags=["Categories"])
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.put("/categories/{category_id}", response_model=schemas.Category, tags=["Categories"])
def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.update_category(db, category_id=category_id, category_update=category_update)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# AD ENDPOINTS
@app.post("/ads/", response_model=schemas.AdResponse, tags=["Ads"])
def create_ad(ad: schemas.AdCreate, db: Session = Depends(get_db)):
    return crud.create_ad(db=db, ad=ad)

@app.get("/ads/", response_model=List[schemas.AdResponse], tags=["Ads"])
def read_ads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.get_ads(db, skip=skip, limit=limit)
    return ads

@app.get("/ads/search", response_model=List[schemas.AdResponse], tags=["Ads"])
def search_ads(q: str = Query(..., description="Search query"), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.search_ads(db, query=q, skip=skip, limit=limit)
    return ads

@app.get("/ads/user/{user_id}", response_model=List[schemas.AdResponse], tags=["Ads"])
def read_user_ads(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.get_ads_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return ads

@app.get("/ads/category/{category_id}", response_model=List[schemas.AdResponse], tags=["Ads"])
def read_ads_by_category(category_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.get_ads_by_category(db, category_id=category_id, skip=skip, limit=limit)
    return ads

@app.get("/ads/location/{location_id}", response_model=List[schemas.AdResponse], tags=["Ads"])
def read_ads_by_location(location_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.get_ads_by_location(db, location_id=location_id, skip=skip, limit=limit)
    return ads

@app.get("/ads/{ad_id}", response_model=schemas.AdResponse, tags=["Ads"])
def read_ad(ad_id: int, db: Session = Depends(get_db)):
    db_ad = crud.get_ad(db, ad_id=ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return db_ad

@app.put("/ads/{ad_id}", response_model=schemas.AdResponse, tags=["Ads"])
def update_ad(ad_id: int, ad_update: schemas.AdUpdate, db: Session = Depends(get_db)):
    db_ad = crud.update_ad(db, ad_id=ad_id, ad_update=ad_update)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return db_ad

@app.delete("/ads/{ad_id}", tags=["Ads"])
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    db_ad = crud.delete_ad(db, ad_id=ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return {"message": "Ad deleted successfully"}

# AD IMAGE ENDPOINTS
@app.post("/ad-images/", response_model=schemas.AdImage, tags=["Ad Images"])
def create_ad_image(ad_image: schemas.AdImageCreate, db: Session = Depends(get_db)):
    return crud.create_ad_image(db=db, ad_image=ad_image)

@app.get("/ads/{ad_id}/images", response_model=List[schemas.AdImage], tags=["Ad Images"])
def read_ad_images(ad_id: int, db: Session = Depends(get_db)):
    images = crud.get_ad_images(db, ad_id=ad_id)
    return images

@app.delete("/ad-images/{image_id}", tags=["Ad Images"])
def delete_ad_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.delete_ad_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}

# FAVORITE ENDPOINTS
@app.post("/favorites/", response_model=schemas.Favorite, tags=["Favorites"])
def create_favorite(favorite: schemas.FavoriteCreate, db: Session = Depends(get_db)):
    return crud.create_favorite(db=db, favorite=favorite)

@app.get("/users/{user_id}/favorites", response_model=List[schemas.Favorite], tags=["Favorites"])
def read_user_favorites(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    favorites = crud.get_user_favorites(db, user_id=user_id, skip=skip, limit=limit)
    return favorites

@app.delete("/favorites/{user_id}/{ad_id}", tags=["Favorites"])
def delete_favorite(user_id: int, ad_id: int, db: Session = Depends(get_db)):
    db_favorite = crud.delete_favorite(db, user_id=user_id, ad_id=ad_id)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Favorite removed successfully"}

@app.get("/favorites/{user_id}/{ad_id}", tags=["Favorites"])
def check_favorite(user_id: int, ad_id: int, db: Session = Depends(get_db)):
    is_fav = crud.is_favorite(db, user_id=user_id, ad_id=ad_id)
    return {"is_favorite": is_fav}

# MESSAGE ENDPOINTS
@app.post("/messages/", response_model=schemas.Message, tags=["Messages"])
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@app.get("/ads/{ad_id}/messages", response_model=List[schemas.Message], tags=["Messages"])
def read_ad_messages(ad_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages_for_ad(db, ad_id=ad_id, skip=skip, limit=limit)
    return messages

@app.get("/conversations/{user1_id}/{user2_id}/{ad_id}", response_model=List[schemas.Message], tags=["Messages"])
def read_conversation(user1_id: int, user2_id: int, ad_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_conversation(db, user1_id=user1_id, user2_id=user2_id, ad_id=ad_id, skip=skip, limit=limit)
    return messages

@app.get("/users/{user_id}/messages", response_model=List[schemas.Message], tags=["Messages"])
def read_user_messages(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_user_messages(db, user_id=user_id, skip=skip, limit=limit)
    return messages

@app.put("/messages/{message_id}", response_model=schemas.Message, tags=["Messages"])
def update_message(message_id: int, message_update: schemas.MessageUpdate, db: Session = Depends(get_db)):
    db_message = crud.update_message(db, message_id=message_id, message_update=message_update)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.delete("/messages/{message_id}", tags=["Messages"])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.delete_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

# REPORT ENDPOINTS
@app.post("/reports/", response_model=schemas.Report, tags=["Reports"])
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db=db, report=report)

@app.get("/reports/", response_model=List[schemas.Report], tags=["Reports"])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = crud.get_reports(db, skip=skip, limit=limit)
    return reports

@app.get("/ads/{ad_id}/reports", response_model=List[schemas.Report], tags=["Reports"])
def read_ad_reports(ad_id: int, db: Session = Depends(get_db)):
    reports = crud.get_reports_for_ad(db, ad_id=ad_id)
    return reports

@app.delete("/reports/{report_id}", tags=["Reports"])
def delete_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.delete_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Report deleted successfully"}

# TRANSACTION ENDPOINTS
@app.post("/transactions/", response_model=schemas.Transaction, tags=["Transactions"])
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=List[schemas.Transaction], tags=["Transactions"])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.get("/users/{user_id}/transactions/buyer", response_model=List[schemas.Transaction], tags=["Transactions"])
def read_user_buyer_transactions(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.get_user_transactions_as_buyer(db, user_id=user_id, skip=skip, limit=limit)
    return transactions

@app.get("/users/{user_id}/transactions/seller", response_model=List[schemas.Transaction], tags=["Transactions"])
def read_user_seller_transactions(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.get_user_transactions_as_seller(db, user_id=user_id, skip=skip, limit=limit)
    return transactions

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def update_transaction(transaction_id: int, transaction_update: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = crud.update_transaction(db, transaction_id=transaction_id, transaction_update=transaction_update)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.delete("/transactions/{transaction_id}", tags=["Transactions"])
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.delete_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 