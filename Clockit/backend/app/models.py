from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
 
 
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    listings = relationship("Listing", back_populates="seller")
    cart = relationship("Cart", back_populates="user", uselist=False)
 
 
class Event(Base):
    __tablename__ = "events"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    venue = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    listings = relationship("Listing", back_populates="event")
 
 
class Listing(Base):
    __tablename__ = "listings"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_type = Column(String(100))
    section = Column(String(50))
    row_name = Column(String(20))
    seat = Column(String(20))
    quantity_available = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), server_default="EUR")
    status = Column(String(20), server_default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    event = relationship("Event", back_populates="listings")
    seller = relationship("User", back_populates="listings")
 
 
class Cart(Base):
    __tablename__ = "cart"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
 
 
class CartItem(Base):
    __tablename__ = "cart_items"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price_snapshot = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    __table_args__ = (UniqueConstraint("cart_id", "listing_id", name="uq_cart_listing"),)
 
    cart = relationship("Cart", back_populates="items")
    listing = relationship("Listing")