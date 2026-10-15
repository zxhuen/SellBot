"""add unique constraint to chat sessions

Revision ID: 5232c4ef2cae
Revises: b7a86aef95af
Create Date: 2026-10-15 11:35:20.156183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5232c4ef2cae'
down_revision: Union[str, Sequence[str], None] = 'b7a86aef95af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
