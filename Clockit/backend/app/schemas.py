from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
 
 
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    display_name: str
 
 
class UserLogin(BaseModel):
    email: EmailStr
    password: str
 
 
class UserOut(BaseModel):
    id: int
    email: str
    display_name: str
    created_at: datetime
 
    class Config:
        from_attributes = True
 
 
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
 
 
class EventOut(BaseModel):
    id: int
    title: str
    venue: str
    city: str
    starts_at: datetime
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
 
    class Config:
        from_attributes = True
 
 
class EventListOut(BaseModel):
    events: List[EventOut]
    total: int
    page: int
    per_page: int
 
 
class ListingCreate(BaseModel):
    event_id: int
    ticket_type: Optional[str] = None
    section: Optional[str] = None
    row_name: Optional[str] = None
    seat: Optional[str] = None
    quantity_available: int
    price: Decimal
    currency: str = "EUR"
 
 
class ListingOut(BaseModel):
    id: int
    event_id: int
    seller_id: int
    ticket_type: Optional[str] = None
    section: Optional[str] = None
    row_name: Optional[str] = None
    seat: Optional[str] = None
    quantity_available: int
    price: Decimal
    currency: str
    status: str
    created_at: datetime
    seller_name: Optional[str] = None
    event_title: Optional[str] = None
 
    class Config:
        from_attributes = True
 
 
class CartItemAdd(BaseModel):
    listing_id: int
    quantity: int
 
 
class CartItemUpdate(BaseModel):
    quantity: int
 
 
class CartItemOut(BaseModel):
    id: int
    listing_id: int
    quantity: int
    unit_price_snapshot: Decimal
    event_title: Optional[str] = None
    ticket_type: Optional[str] = None
    listing_status: Optional[str] = None
 
    class Config:
        from_attributes = True
 
 
class CartOut(BaseModel):
    id: int
    items: List[CartItemOut]
    total: Decimal
 
    class Config:
        from_attributes = True