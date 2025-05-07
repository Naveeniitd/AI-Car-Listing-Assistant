from sqlalchemy import Column, Integer, String, JSON
from app.core.config import Base  # Base from SQLAlchemy declarative_base()

class CarListing(Base):
    __tablename__ = "car_listings"
    
    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    images = Column(JSON)  # Stores paths to images
    metadata = Column(JSON)  # Additional user-provided data
    status = Column(String, default="processing")