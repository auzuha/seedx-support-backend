from passlib.context import CryptContext
from app.models import User
from app.utils.jwt_util import create_access_token
from app.database import SessionLocal
from sqlalchemy.orm import Session

#create a hash function to hash user passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    """
    Function to get a user by their email.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str, role: str):
    """
    Function to create a user, and store the details in the database.
    """

    #hash the user's password
    hashed_password = pwd_context.hash(password)
    db_user = User(email=email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Function to verify user's details.
    """
    user = get_user_by_email(db, email)
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None

def login_user(db: Session, email: str, password: str):
    """
    Function to return an access token for the user.
    """
    user = authenticate_user(db, email, password)
    if user:
        access_token = create_access_token(
            data={"email": user.email,"id":str(user.id),"role":user.role}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    return None
