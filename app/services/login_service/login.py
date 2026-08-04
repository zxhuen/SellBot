from sqlalchemy.orm import Session
from app.schemas import PersonCreate
from fastapi import HTTPException
import logging
from app.core.supabse_bucket import supabase
from app.models.User import User
from app.models.User_Usage import UserUsage


def login_user(token: str, db: Session):
    try:
        auth_user = supabase.auth.get_user(token).user

        if auth_user is None:
            raise HTTPException(status_code=404, detail="Invalid token.")

        user = db.query(User).filter(User.id == auth_user.id).first()

        if user is None:
            user = User(
                id=auth_user.id,
                email=auth_user.email,
                display_name=auth_user.user_metadata.get("full_name", ""),
                avatar_url=auth_user.user_metadata.get("avatar_url"),
                subscription_id=1,
            )

            db.add(user)
            db.flush()  # Makes the user available before creating related rows

            usage = UserUsage(
                user_id=user.id,
                products_created_today=0,
            )

            db.add(usage)
            db.commit()
            db.refresh(user)

        return user

    except Exception as e:
        db.rollback()
        print(repr(e))
        raise
