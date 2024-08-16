from sqlalchemy.orm import Session

from web_hw_13_api.src.database.models import User
from web_hw_13_api.src.schemas import UserModel


async def create_user(db: Session, body: UserModel) -> User:
    user = User(**body.__dict__)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter_by(email=email).first()


async def update_token(db: Session, user: User, token: str | None) -> None:
    user.update_token = token
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(db, email)
    user.avatar = url
    db.commit()
    return user


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(db, email)
    user.email_confirmed = True
    db.commit()

