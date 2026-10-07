from fastapi import APIRouter,Depends,HTTPException,Request
from app.schemas import UserCreate,UserResponse,LoginCreate,LoginResponse
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.security import hash_password,verify_password, create_access_token
from app.limiter import limiter
from logging_config import logger

router=APIRouter()


@router.post("/register",response_model=UserResponse)
def register(user:UserCreate , db:Session=Depends(get_db)):
    db_username=db.query(User).filter(User.username==user.username).first()
    if db_username:
        raise HTTPException(status_code=409, detail="Username already exist")
    hashed_password=hash_password(user.password)
    new_user=User(
        username=user.username,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
def login(request:Request,login:LoginCreate , db:Session=Depends(get_db)):
    db_login=db.query(User).filter(User.username==login.username).first()
    if not db_login:
        logger.warning("Failed login attempt")
        raise HTTPException(status_code=401 , detail="Invalid username or password")
    if not verify_password(login.password,db_login.password_hash):
        logger.warning("Failed login attempt")
        raise HTTPException(status_code=401 , detail="Invalid username or password")
    token=create_access_token(db_login.id)
    logger.info("User logged in successfully")
    return{
        "access_token":token,
        "token_type":"bearer"
    }
        


