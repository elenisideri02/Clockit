"""Idempotent seed data for development."""
 
from datetime import datetime, timezone, timedelta
from app.database import SessionLocal
from app.models import User, Event, Listing
from app.auth import hash_password
 
 
def seed():
    db = SessionLocal()
    try:
        if db.query(User).first():
            print("[seed] Data already exists, skipping.")
            return
 
        print("[seed] Seeding database...")
 
        seller = User(email="seller@clockit.com", hashed_password=hash_password("password123"), display_name="Demo Seller")
        buyer = User(email="buyer@clockit.com", hashed_password=hash_password("password123"), display_name="Demo Buyer")
        db.add_all([seller, buyer])
        db.flush()
 
        now = datetime.now(timezone.utc)
        events_data = [
            Event(
                title="Athens Rock Festival 2026",
                venue="OAKA Stadium",
                city="Athens",
                starts_at=now + timedelta(days=80),
                category="Music",
                description="The biggest rock festival in Greece featuring international and local bands across three stages.",
            ),
            Event(
                title="Thessaloniki Jazz Night",
                venue="Thessaloniki Concert Hall",
                city="Thessaloniki",
                starts_at=now + timedelta(days=25),
                category="Music",
                description="An unforgettable evening of jazz performances by award-winning artists from around the world.",
            ),
            Event(
                title="Antigone - Greek Theatre",
                venue="Odeon of Herodes Atticus",
                city="Athens",
                starts_at=now + timedelta(days=45),
                category="Theatre",
                description="Sophocles' timeless tragedy performed under the stars at the historic Odeon of Herodes Atticus.",
            ),
            Event(
                title="EuroBasket Quarter Finals",
                venue="Peace & Friendship Stadium",
                city="Athens",
                starts_at=now + timedelta(days=100),
                category="Sports",
                description="Watch the best basketball teams in Europe compete in the quarter-final stage of EuroBasket 2026.",
            ),
            Event(
                title="DJ Marathon Mykonos",
                venue="Paradise Club",
                city="Mykonos",
                starts_at=now + timedelta(days=130),
                category="Music",
                description="A 12-hour DJ marathon featuring the hottest electronic music acts on the island.",
            ),
            Event(
                title="Stand-Up Comedy Night",
                venue="Gazarte",
                city="Athens",
                starts_at=now + timedelta(days=20),
                category="Comedy",
                description="A hilarious evening of stand-up comedy with Greece's finest comedians and special international guests.",
            ),
            Event(
                title="Greek Opera Gala",
                venue="Megaron Mousikis",
                city="Athens",
                starts_at=now + timedelta(days=60),
                category="Music",
                description="A spectacular gala evening featuring arias and orchestral works by the Greek National Opera.",
            ),
            Event(
                title="Panathinaikos vs Olympiacos",
                venue="OAKA Stadium",
                city="Athens",
                starts_at=now + timedelta(days=35),
                category="Sports",
                description="The eternal derby of Greek football. Experience the passion of the biggest rivalry in Greece.",
            ),
        ]
        db.add_all(events_data)
        db.flush()
 
        listings_data = [
            Listing(event_id=events_data[0].id, seller_id=seller.id, ticket_type="General Admission", quantity_available=10, price=45.00),
            Listing(event_id=events_data[0].id, seller_id=seller.id, ticket_type="VIP", section="A", quantity_available=4, price=120.00),
            Listing(event_id=events_data[0].id, seller_id=seller.id, ticket_type="Backstage Pass", quantity_available=2, price=250.00),
            Listing(event_id=events_data[1].id, seller_id=seller.id, ticket_type="Standard", section="Balcony", quantity_available=6, price=35.00),
            Listing(event_id=events_data[1].id, seller_id=seller.id, ticket_type="Front Row", section="Orchestra", row_name="A", quantity_available=2, price=80.00),
            Listing(event_id=events_data[2].id, seller_id=seller.id, ticket_type="Standard", section="Upper", quantity_available=8, price=30.00),
            Listing(event_id=events_data[2].id, seller_id=seller.id, ticket_type="Premium", section="Lower", row_name="C", quantity_available=3, price=65.00),
            Listing(event_id=events_data[3].id, seller_id=seller.id, ticket_type="Category A", section="East Stand", quantity_available=5, price=55.00),
            Listing(event_id=events_data[3].id, seller_id=seller.id, ticket_type="Category B", section="North Stand", quantity_available=12, price=35.00),
            Listing(event_id=events_data[4].id, seller_id=seller.id, ticket_type="General Entry", quantity_available=20, price=40.00),
            Listing(event_id=events_data[4].id, seller_id=seller.id, ticket_type="VIP Table", quantity_available=2, price=200.00),
            Listing(event_id=events_data[5].id, seller_id=seller.id, ticket_type="Standard", quantity_available=15, price=20.00),
            Listing(event_id=events_data[5].id, seller_id=seller.id, ticket_type="Front Row", row_name="1", quantity_available=4, price=40.00),
            Listing(event_id=events_data[6].id, seller_id=seller.id, ticket_type="Stalls", section="Stalls", quantity_available=6, price=50.00),
            Listing(event_id=events_data[6].id, seller_id=seller.id, ticket_type="Grand Circle", section="Circle", quantity_available=10, price=35.00),
            Listing(event_id=events_data[7].id, seller_id=seller.id, ticket_type="Gate 13", section="South Stand", quantity_available=8, price=25.00),
            Listing(event_id=events_data[7].id, seller_id=seller.id, ticket_type="VIP Box", section="West Stand", quantity_available=2, price=150.00),
        ]
        db.add_all(listings_data)
        db.commit()
        print(f"[seed] Created {len(events_data)} events, {len(listings_data)} listings, 2 users.")
 
    except Exception as e:
        db.rollback()
        print(f"[seed] Error: {e}")
        raise
    finally:
        db.close()
 
 
if __name__ == "__main__":
    seed()
 