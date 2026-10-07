from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from fastapi import Depends,HTTPException
from app.security import SECRET_KEY,ALGORITHM
from app.models import User
from sqlalchemy.orm import Session
from logging_config import logger
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    try:
        
      payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        logger.warning("Invalid or expired jwt token")
        raise HTTPException(status_code=401 , detail="Invalid or expired token")
    if "sub" not in payload:
        logger.warning("Jwt token missing subject")
        raise HTTPException(status_code=401 , detail="Invalid token")
    try:
        user_id=int(payload["sub"])
    except(ValueError,TypeError):
        logger.warning("Invalid user ID in jwt token")
        raise HTTPException(status_code=401 , detail="Invalid token")
    
    db_get_user=db.query(User).filter(User.id==user_id).first()
    if not db_get_user:
        logger.warning("Authenticated user not found")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return db_get_user
