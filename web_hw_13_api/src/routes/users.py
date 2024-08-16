import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from web_hw_13_api.src.Settings import settings
from web_hw_13_api.src.database.db import get_db
from web_hw_13_api.src.database.models import User
from web_hw_13_api.src.schemas import UserDb
from web_hw_13_api.src.services.auth import auth_service
import web_hw_13_api.src.repository.users as repository_users

router = APIRouter(prefix="/users")


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.name}', overwrite=True)
    src_url = cloudinary.CloudinaryResource(f'NotesApp/{current_user.name}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
