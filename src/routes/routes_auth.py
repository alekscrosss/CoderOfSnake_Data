# file routers/comments.py
from typing import List

from fastapi import Depends, HTTPException, status,  APIRouter,  Security, BackgroundTasks, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from src.db.database import get_db
from src.schemas.schemas_user import UserModel, UserResponse, TokenModel, RequestEmail
from src.crud import crud_users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import Request
from src.db.models import User
from fastapi.security import OAuth2PasswordRequestForm
from src.crud.user_current import get_current_user
from fastapi.responses import Response
from ipaddress import ip_address 
from typing import Callable 
from fastapi.responses import JSONResponse 

router = APIRouter(prefix="/auth", tags=['auth'])
security = HTTPBearer()

app = FastAPI() 
templates = Jinja2Templates(directory='templates')

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    # return new_user
  # Redirect to login page after successful registration
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    #якщо емейл не підтверджений  нас не пусте залогіниться
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/home")
async def home(request: Request, current_user: User = Depends(get_current_user)):
    username = current_user.username
    return templates.TemplateResponse("home.html", {"request": request, "username": username})

@router.get("/confirmation", response_class=HTMLResponse)
async def confirmation_page(request: Request):
    return templates.TemplateResponse("confirmation.html", {"request": request})

router.get("/logout")
async def logout(request: Request, response: Response):
    # Видалення cookie з токеном доступу
    response.delete_cookie("access_token")
    return templates.TemplateResponse("index.html", {"request": request, "message": "Ви успішно вийшли з системи"})


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}', response_class=HTMLResponse)
async def confirmed_email(token: str, db: Session = Depends(get_db)):

    email =  auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return templates.TemplateResponse('confirmation_result.html', {"request": request, "message": "Your email is already confirmed. Redirecting to login...", "url": "/login"})
    await repository_users.confirmed_email(email, db)
    return templates.TemplateResponse('confirmation_result.html', {"request": request, "message": "Email confirmed. Redirecting to login...", "url": "/login"})

@router.post('/request_email', response_class=HTMLResponse)
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):

    user = await repository_users.get_user_by_email(body.email, db)

    if user and user.confirmed:
        return templates.TemplateResponse("confirmation.html", {"request": request})
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}
