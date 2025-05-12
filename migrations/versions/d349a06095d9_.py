"""empty message

Revision ID: d349a06095d9
Revises: 16bebfa9e0da
Create Date: 2025-05-12 12:48:33.812773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd349a06095d9'
down_revision: Union[str, None] = '16bebfa9e0da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
