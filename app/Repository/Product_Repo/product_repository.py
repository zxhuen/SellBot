from app.models import Product
from app.models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from uuid import UUID
from app.models.ChatSession import ChatSession
from app.models.Message import Message
from sqlalchemy.ext.asyncio import AsyncSession



def list_product_repo(user: User, db: Session):
    stmt = select(Product).where(Product.owner_id == user.id)

    result = db.execute(stmt)

    return result.scalars().all()


def get_product(user: User, id: UUID, db: Session):
    stmt = select(Product).where(
        Product.owner_id == user.id,
        Product.id == id,
    )

    result = db.execute(stmt)

    return result.scalars().first()



def get_product_public_id(public_id: UUID, db: Session):
    stmt = select(Product).where(
        Product.public_id == public_id,
    )

    result = db.execute(stmt)

    return result.scalars().first()

def mark_product_as_sold(id: UUID, user: User, db: Session):
    stmt = (
        select(Product)
        .where(
            Product.id == id,
            Product.owner_id == user.id,
        )
        .with_for_update()
    )

    result = db.execute(stmt)

    return result.scalars().first()


def get_product_chat_session(
    db: Session,
    product_id: UUID,
    user_id: UUID,
):
    stmt = (
        select(ChatSession)
        .options(
            joinedload(ChatSession.product),
            joinedload(ChatSession.user),
        )
        .where(
            ChatSession.product_id == product_id,
            ChatSession.product.has(Product.owner_id == user_id),
        )
        .order_by(desc(ChatSession.last_message_at))
    )

    result = db.execute(stmt)
    return result.scalars().all()



async def get_chat_messages(
    db: AsyncSession,
    chat_session_id: UUID,
    user_id: UUID,
):
    stmt = (
        select(Message)
        .join(Message.chat_session)
        .join(ChatSession.product)
        .where(
            Message.chat_session_id == chat_session_id,
            Product.owner_id == user_id,
        )
        .order_by(Message.created_at.asc())
    )

    result = await db.execute(stmt)
    return result.scalars().all()
