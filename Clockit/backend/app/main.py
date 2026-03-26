from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import auth_router, events_router, listings_router, cart_router
 
app = FastAPI(title="Clockit API", version="1.0.0")
 
app.include_router(auth_router.router)
app.include_router(events_router.router)
app.include_router(listings_router.router)
app.include_router(cart_router.router)
 
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
 
 
@app.get("/")
async def index():
    return FileResponse("frontend/index.html")
 
 
@app.get("/events.html")
async def events_page():
    return FileResponse("frontend/events.html")
 
 
@app.get("/event.html")
async def event_page():
    return FileResponse("frontend/event.html")
 
 
@app.get("/login.html")
async def login_page():
    return FileResponse("frontend/login.html")
 
 
@app.get("/sell.html")
async def sell_page():
    return FileResponse("frontend/sell.html")
 
 
@app.get("/my-listings.html")
async def my_listings_page():
    return FileResponse("frontend/my-listings.html")
 
 
@app.get("/cart.html")
async def cart_page():
    return FileResponse("frontend/cart.html")
 
 
@app.get("/about.html")
async def about_page():
    return FileResponse("frontend/about.html")
 
 
@app.get("/help.html")
async def help_page():
    return FileResponse("frontend/help.html")