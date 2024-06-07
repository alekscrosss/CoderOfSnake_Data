# file main.py
import os
import time

import redis
from fastapi import Request
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.responses import HTMLResponse
from src.db.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from src.routes import routes_auth

app = FastAPI()

# Монтування папки static
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

# # Fetch the Redis host from environment variable
# REDIS_HOST = os.environ.get("REDIS_HOST")
#
# # Fetch the Redis port from environment variable, defaulting to 6380 if not set
# REDIS_PORT = int(os.environ.get("REDIS_PORT", 11929))
# REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
#
# # Create the Redis client
# redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

@app.middleware('http')
async def custom_middleware(request: Request, call_next):

    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['performance'] = str(during)
    return response


# Додавання обробника для кореневого URL
@app.get("/", response_class=HTMLResponse, description="Main page")
async def root(request: Request):

    return templates.TemplateResponse('index.html', {"request": request, "title": "Car numbers aрр"})

# Route for registration form
@app.get("/signup", response_class=HTMLResponse, description="Sign Up Page")
async def signup_page(request: Request):
    return templates.TemplateResponse('signup.html', {"request": request, "title": "Sign Up"})

# Route for login form
@app.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/confirmation", response_class=HTMLResponse)
async def confirmation_page(request: Request):
    return templates.TemplateResponse('confirmation.html', {"request": request, "title": "Email Confirmation"})


@app.get("/home", response_class=HTMLResponse)
async def confirmation_page(request: Request):
    return templates.TemplateResponse('home.html', {"request": request, "title": "Email Confirmation"})


@app.get("/logout")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Car numbers aрр"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):

    try:
    #Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")






app.include_router(routes_auth.router, prefix='/api')

