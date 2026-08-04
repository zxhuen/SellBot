from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Depends
from app.core.supabse_bucket import supabase
from app.models import User, UserUsage
from app.core.security import oauth2_scheme
from app.core.database import get_db


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        response = supabase.auth.get_user(token)
        auth_user = response.user

        if auth_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token.",
            )

        user = (
            db.query(User)
            .filter(User.id == auth_user.id)
            .options(joinedload(User.subscription), joinedload(User.usage))
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found.",
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
        )
