# Clockit - Last-Minute Ticket Marketplace
 
A full-stack web application for buying and selling last-minute event tickets in Greece.
 
## Architecture
 
```
clockit/
├── docker-compose.yml          # Orchestrates PostgreSQL + Backend
├── .env.example                # Environment variable template
├── backend/
│   ├── Dockerfile              # Python 3.12 container
│   ├── requirements.txt        # Python dependencies
│   ├── alembic.ini             # Alembic configuration
│   ├── alembic/                # Database migrations
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial_tables.py
│   └── app/
│       ├── main.py             # FastAPI app + static file serving
│       ├── config.py           # Settings from environment
│       ├── database.py         # SQLAlchemy engine + session
│       ├── models.py           # ORM models (User, Event, Listing, Cart, CartItem)
│       ├── schemas.py          # Pydantic request/response schemas
│       ├── auth.py             # JWT auth + password hashing
│       ├── seed.py             # Idempotent seed data
│       └── routers/
│           ├── auth_router.py      # POST /api/auth/register, /login, GET /me
│           ├── events_router.py    # GET /api/events, /{id}, /{id}/listings, /categories, /cities
│           ├── listings_router.py  # POST /api/listings, GET /my, PATCH /{id}/deactivate
│           └── cart_router.py      # GET /api/cart, POST/PATCH/DELETE /items
├── frontend/
│   ├── index.html              # Landing page with hero + featured events
│   ├── events.html             # Browse events with search/filter/sort/pagination
│   ├── event.html              # Event detail + available ticket listings
│   ├── login.html              # Login + Register forms
│   ├── sell.html               # Create a new listing (seller flow)
│   ├── my-listings.html        # View/deactivate own listings
│   ├── cart.html               # Cart view (terminal state)
│   ├── about.html              # About page
│   ├── help.html               # FAQ page
│   ├── css/styles.css          # Full CSS with Clockit palette
│   ├── js/
│   │   ├── i18n.js             # Bilingual EN/EL dictionary + translator
│   │   ├── api.js              # Fetch wrapper with JWT headers
│   │   ├── auth.js             # Auth state management
│   │   ├── nav.js              # Dynamic navigation + footer + toasts
│   │   ├── app.js              # Home page logic
│   │   ├── events.js           # Events browsing + filters
│   │   ├── event-detail.js     # Event detail + listings
│   │   ├── cart.js             # Cart operations
│   │   ├── sell.js             # Listing creation
│   │   └── my-listings.js      # Seller dashboard
│   └── assets/                 # Place logo images here
```
 
## Tech Stack
 
- **Database**: PostgreSQL 16
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, python-jose (JWT), passlib (bcrypt)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3 (no frameworks)
- **Infrastructure**: Docker Compose
 
## How to Run
 
### Prerequisites
 
- Docker Desktop for Windows (running)
 
### Steps
 
1. **Place your logo file**:
   Copy your Clockit logo image to `frontend/assets/clockit-logo.png`
 
2. **Start the application**:
   ```bash
   cd clockit
   docker compose up --build
   ```
 
3. **Open the app**:
   Navigate to [http://localhost:8000](http://localhost:8000)
 
   On first startup, the backend will:
   - Run Alembic migrations (create all database tables)
   - Seed the database with sample events, listings, and demo users
 
### Demo Accounts
 
| Email               | Password      | Role   |
|---------------------|---------------|--------|
| seller@clockit.com  | password123   | Seller |
| buyer@clockit.com   | password123   | Buyer  |
 
## Environment Variables to Configure
 
These are set in `docker-compose.yml`. For production, change them:
 
| Variable       | File                 | Current Value                                  | Description                                         |
|----------------|----------------------|------------------------------------------------|-----------------------------------------------------|
| `JWT_SECRET`   | `docker-compose.yml` | `clockit-dev-secret-change-in-prod`            | **MUST CHANGE** - Secret key for signing JWT tokens. Use a random 32+ char string. |
| `DATABASE_URL` | `docker-compose.yml` | `postgresql://clockit:clockit@db:5432/clockit` | PostgreSQL connection string. Change user/password for production. |
| `POSTGRES_USER`     | `docker-compose.yml` | `clockit`                               | Database username. Change for production.           |
| `POSTGRES_PASSWORD` | `docker-compose.yml` | `clockit`                               | **MUST CHANGE** - Database password.                |
| `POSTGRES_DB`       | `docker-compose.yml` | `clockit`                               | Database name.                                      |
 
## User Flow (per workflow diagram)
 
1. **Landing Page** → Hero section + featured events
2. **Browse Events** → Search, filter by category/city, sort, paginate
3. **Event Detail** → View event info + available ticket listings
4. **Add to Cart** → Select quantity, add listing to cart → redirects to cart page
5. **Cart** → View items, update quantities, remove items, clear cart
6. **Sell Tickets** → Authenticated users can create listings (select event, set details & price)
7. **My Listings** → View own listings, deactivate active ones
8. **Auth** → Register / Login with JWT tokens
9. **Language Toggle** → Switch between English and Greek (persisted in localStorage)
 
**Flow ends at cart** - No checkout, payment, or order placement is implemented.
 
## API Endpoints
 
### Auth
- `POST /api/auth/register` - Create account, returns JWT
- `POST /api/auth/login` - Login, returns JWT
- `GET /api/auth/me` - Get current user (requires auth)
 
### Events
- `GET /api/events` - List events (query: search, category, city, sort_by, page, per_page)
- `GET /api/events/categories` - Distinct categories
- `GET /api/events/cities` - Distinct cities
- `GET /api/events/{id}` - Event detail
- `GET /api/events/{id}/listings` - Active listings for event
 
### Listings
- `POST /api/listings` - Create listing (requires auth)
- `GET /api/listings/my` - Current user's listings (requires auth)
- `PATCH /api/listings/{id}/deactivate` - Deactivate listing (requires auth, owner only)
 
### Cart
- `GET /api/cart` - Get cart with items (requires auth)
- `POST /api/cart/items` - Add item to cart (requires auth)
- `PATCH /api/cart/items/{id}` - Update quantity (requires auth)
- `DELETE /api/cart/items/{id}` - Remove item (requires auth)
- `DELETE /api/cart` - Clear cart (requires auth)
 
## Database Schema
 
Five tables: `users`, `events`, `listings`, `cart`, `cart_items` with proper foreign keys and constraints. See `backend/alembic/versions/001_initial_tables.py` for the full schema.
 
## Bilingual Support (EN/EL)
 
All user-facing strings are translated. Click the **EN/EL** button in the navigation bar to toggle language. The preference is saved in localStorage.