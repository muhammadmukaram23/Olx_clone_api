# OLX Clone Backend API

A comprehensive FastAPI backend for an OLX-style marketplace application with full CRUD operations for users, ads, categories, locations, messages, favorites, reports, and transactions.

## Features

- **User Management**: Registration, authentication, profile management
- **Ad Management**: Create, read, update, delete ads with images
- **Category System**: Hierarchical categories with parent-child relationships
- **Location Management**: City, state, country-based location system
- **Messaging System**: Chat between buyers and sellers
- **Favorites/Wishlist**: Users can save favorite ads
- **Reporting System**: Report inappropriate ads
- **Transaction Management**: Track buying/selling transactions
- **Search Functionality**: Search ads by title and description

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **MySQL**: Database (via PyMySQL connector)
- **Pydantic**: Data validation using Python type annotations
- **Passlib**: Password hashing with bcrypt
- **Uvicorn**: ASGI server

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
- XAMPP (if using local MySQL)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - Start your MySQL server (XAMPP or standalone)
   - Create a database named `olx_clone`:
     ```sql
     CREATE DATABASE olx_clone;
     ```
   - Run the SQL script from `database.sql` to create tables and insert sample data

4. **Configure Database Connection**:
   - The database credentials are set in `main.py`:
     ```python
     DATABASE_URL = "mysql+pymysql://root:@localhost/olx_clone"
     ```
   - Modify the connection string if your MySQL setup is different

5. **Run the Application**:
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**:
   - API will be available at: `http://localhost:8000`
   - Interactive API documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination)
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Locations
- `POST /locations/` - Create location
- `GET /locations/` - Get all locations
- `GET /locations/{location_id}` - Get location by ID
- `PUT /locations/{location_id}` - Update location
- `DELETE /locations/{location_id}` - Delete location

### Categories
- `POST /categories/` - Create category
- `GET /categories/` - Get all categories
- `GET /categories/parent` - Get parent categories only
- `GET /categories/{category_id}/subcategories` - Get subcategories
- `GET /categories/{category_id}` - Get category by ID
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category

### Ads
- `POST /ads/` - Create new ad
- `GET /ads/` - Get all ads (with pagination)
- `GET /ads/search?q={query}` - Search ads
- `GET /ads/user/{user_id}` - Get ads by user
- `GET /ads/category/{category_id}` - Get ads by category
- `GET /ads/location/{location_id}` - Get ads by location
- `GET /ads/{ad_id}` - Get ad by ID
- `PUT /ads/{ad_id}` - Update ad
- `DELETE /ads/{ad_id}` - Delete ad

### Ad Images
- `POST /ad-images/` - Add image to ad
- `GET /ads/{ad_id}/images` - Get all images for an ad
- `DELETE /ad-images/{image_id}` - Delete image

### Favorites
- `POST /favorites/` - Add ad to favorites
- `GET /users/{user_id}/favorites` - Get user's favorites
- `GET /favorites/{user_id}/{ad_id}` - Check if ad is favorited
- `DELETE /favorites/{user_id}/{ad_id}` - Remove from favorites

### Messages
- `POST /messages/` - Send message
- `GET /ads/{ad_id}/messages` - Get messages for an ad
- `GET /conversations/{user1_id}/{user2_id}/{ad_id}` - Get conversation
- `GET /users/{user_id}/messages` - Get user's messages
- `PUT /messages/{message_id}` - Update message
- `DELETE /messages/{message_id}` - Delete message

### Reports
- `POST /reports/` - Report an ad
- `GET /reports/` - Get all reports
- `GET /ads/{ad_id}/reports` - Get reports for an ad
- `DELETE /reports/{report_id}` - Delete report

### Transactions
- `POST /transactions/` - Create transaction
- `GET /transactions/` - Get all transactions
- `GET /transactions/{transaction_id}` - Get transaction by ID
- `GET /users/{user_id}/transactions/buyer` - Get user's buyer transactions
- `GET /users/{user_id}/transactions/seller` - Get user's seller transactions
- `PUT /transactions/{transaction_id}` - Update transaction
- `DELETE /transactions/{transaction_id}` - Delete transaction

## File Structure

```
olx_endpoints/
├── main.py          # FastAPI application and endpoints
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic schemas for request/response
├── crud.py          # Database CRUD operations
├── requirements.txt # Python dependencies
├── database.sql     # Database schema and sample data
└── README.md        # This file
```

## Sample Data

The database comes with sample data including:
- 3 users (Ali Khan, Sara Malik, Ahmed Raza)
- 3 locations (Lahore, Karachi, Islamabad)
- 5 categories (Electronics, Mobiles, Vehicles, Cars, Home Appliances)
- 3 sample ads (iPhone, Honda Civic, Air Conditioner)
- Sample images, favorites, messages, reports, and transactions

## Authentication

Currently, the API uses basic password hashing with bcrypt. For production use, consider implementing:
- JWT tokens for authentication
- Session management
- Role-based access control
- API rate limiting

## Error Handling

The API includes proper error handling with appropriate HTTP status codes:
- 400: Bad Request (validation errors)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error

## Development

To extend the API:
1. Add new models in `models.py`
2. Create corresponding schemas in `schemas.py`
3. Implement CRUD operations in `crud.py`
4. Add endpoints in `main.py`

## Production Deployment

For production deployment:
1. Use environment variables for database credentials
2. Set up proper logging
3. Configure HTTPS
4. Use a production ASGI server like Gunicorn with Uvicorn workers
5. Set up database connection pooling
6. Implement caching (Redis)
7. Add monitoring and health checks 