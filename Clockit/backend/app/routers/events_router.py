from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.database import get_db
from app.models import Event, Listing
from app.schemas import EventOut, EventListOut, ListingOut
 
router = APIRouter(prefix="/api/events", tags=["events"])
 
 
@router.get("", response_model=EventListOut)
def list_events(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("date_asc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    q = db.query(Event)
 
    if search:
        pattern = f"%{search}%"
        q = q.filter(or_(Event.title.ilike(pattern), Event.venue.ilike(pattern), Event.city.ilike(pattern)))
 
    if category:
        q = q.filter(Event.category == category)
 
    if city:
        q = q.filter(Event.city.ilike(f"%{city}%"))
 
    total = q.count()
 
    sort_map = {
        "date_asc": Event.starts_at.asc(),
        "date_desc": Event.starts_at.desc(),
        "title_asc": Event.title.asc(),
        "title_desc": Event.title.desc(),
    }
    q = q.order_by(sort_map.get(sort_by, Event.starts_at.asc()))
 
    events = q.offset((page - 1) * per_page).limit(per_page).all()
    return EventListOut(events=events, total=total, page=page, per_page=per_page)
 
 
@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(Event.category).distinct().order_by(Event.category).all()
    return [r[0] for r in rows]
 
 
@router.get("/cities")
def list_cities(db: Session = Depends(get_db)):
    rows = db.query(Event.city).distinct().order_by(Event.city).all()
    return [r[0] for r in rows]
 
 
@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Event not found")
    return event
 
 
@router.get("/{event_id}/listings")
def get_event_listings(event_id: int, db: Session = Depends(get_db)):
    listings = (
        db.query(Listing)
        .filter(Listing.event_id == event_id, Listing.status == "active")
        .order_by(Listing.price.asc())
        .all()
    )
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
                seller_name=l.seller.display_name if l.seller else None,
            )
        )
    return result