from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Listing, Event, User
from app.schemas import ListingCreate, ListingOut
from app.auth import get_current_user
 
router = APIRouter(prefix="/api/listings", tags=["listings"])
 
 
@router.post("", response_model=ListingOut)
def create_listing(data: ListingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if data.quantity_available < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    if data.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
 
    listing = Listing(
        event_id=data.event_id,
        seller_id=user.id,
        ticket_type=data.ticket_type,
        section=data.section,
        row_name=data.row_name,
        seat=data.seat,
        quantity_available=data.quantity_available,
        price=data.price,
        currency=data.currency,
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return ListingOut(
        id=listing.id,
        event_id=listing.event_id,
        seller_id=listing.seller_id,
        ticket_type=listing.ticket_type,
        section=listing.section,
        row_name=listing.row_name,
        seat=listing.seat,
        quantity_available=listing.quantity_available,
        price=listing.price,
        currency=listing.currency,
        status=listing.status,
        created_at=listing.created_at,
        seller_name=user.display_name,
        event_title=event.title,
    )
 
 
@router.get("/my")
def my_listings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    listings = db.query(Listing).filter(Listing.seller_id == user.id).order_by(Listing.created_at.desc()).all()
    result = []
    for l in listings:
        result.append(
            ListingOut(
                id=l.id,
                event_id=l.event_id,
                seller_id=l.seller_id,
                ticket_type=l.ticket_type,
                section=l.section,
                row_name=l.row_name,
                seat=l.seat,
                quantity_available=l.quantity_available,
                price=l.price,
                currency=l.currency,
                status=l.status,
                created_at=l.created_at,
                seller_name=user.display_name,
                event_title=l.event.title if l.event else None,
            )
        )
    return result
 
 
@router.patch("/{listing_id}/deactivate", response_model=ListingOut)
def deactivate_listing(listing_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Not your listing")
    listing.status = "deactivated"
    db.commit()
    db.refresh(listing)
    return ListingOut(
        id=listing.id,
        event_id=listing.event_id,
        seller_id=listing.seller_id,
        ticket_type=listing.ticket_type,
        section=listing.section,
        row_name=listing.row_name,
        seat=listing.seat,
        quantity_available=listing.quantity_available,
        price=listing.price,
        currency=listing.currency,
        status=listing.status,
        created_at=listing.created_at,
        seller_name=user.display_name,
        event_title=listing.event.title if listing.event else None,
    )
 