"""test8

Revision ID: 20b40ed2e8a6
Revises: 727d2626ff48
Create Date: 2025-12-25 21:30:22.992267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20b40ed2e8a6'
down_revision: Union[str, Sequence[str], None] = '727d2626ff48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
