from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cart, CartItem, Listing, User
from app.schemas import CartItemAdd, CartItemUpdate, CartOut, CartItemOut
from app.auth import get_current_user
 
router = APIRouter(prefix="/api/cart", tags=["cart"])
 
 
def _get_or_create_cart(db: Session, user: User) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart
 
 
def _build_cart_out(cart: Cart) -> CartOut:
    items_out = []
    total = Decimal("0")
    for item in cart.items:
        subtotal = item.unit_price_snapshot * item.quantity
        total += subtotal
        items_out.append(
            CartItemOut(
                id=item.id,
                listing_id=item.listing_id,
                quantity=item.quantity,
                unit_price_snapshot=item.unit_price_snapshot,
                event_title=item.listing.event.title if item.listing and item.listing.event else None,
                ticket_type=item.listing.ticket_type if item.listing else None,
                listing_status=item.listing.status if item.listing else None,
            )
        )
    return CartOut(id=cart.id, items=items_out, total=total)
 
 
@router.get("", response_model=CartOut)
def get_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = _get_or_create_cart(db, user)
    db.refresh(cart)
    return _build_cart_out(cart)
 
 
@router.post("/items", response_model=CartOut)
def add_item(data: CartItemAdd, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    listing = db.query(Listing).filter(Listing.id == data.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.status != "active":
        raise HTTPException(status_code=400, detail="Listing is not active")
    if data.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    if data.quantity > listing.quantity_available:
        raise HTTPException(status_code=400, detail="Not enough tickets available")
 
    cart = _get_or_create_cart(db, user)
    existing = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.listing_id == data.listing_id).first()
 
    if existing:
        new_qty = existing.quantity + data.quantity
        if new_qty > listing.quantity_available:
            raise HTTPException(status_code=400, detail="Not enough tickets available")
        existing.quantity = new_qty
        existing.unit_price_snapshot = listing.price
    else:
        item = CartItem(
            cart_id=cart.id,
            listing_id=data.listing_id,
            quantity=data.quantity,
            unit_price_snapshot=listing.price,
        )
        db.add(item)
 
    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart)
 
 
@router.patch("/items/{item_id}", response_model=CartOut)
def update_item(item_id: int, data: CartItemUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = _get_or_create_cart(db, user)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if data.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
 
    listing = db.query(Listing).filter(Listing.id == item.listing_id).first()
    if listing and data.quantity > listing.quantity_available:
        raise HTTPException(status_code=400, detail="Not enough tickets available")
 
    item.quantity = data.quantity
    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart)
 
 
@router.delete("/items/{item_id}", response_model=CartOut)
def remove_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = _get_or_create_cart(db, user)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart)
 
 
@router.delete("", response_model=CartOut)
def clear_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = _get_or_create_cart(db, user)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart)