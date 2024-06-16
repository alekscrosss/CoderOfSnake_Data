"""Add blacklist

Revision ID: b84ee7d65ffc
Revises: 26c4790c2121
Create Date: 2024-06-15 18:50:29.954503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b84ee7d65ffc'
down_revision: Union[str, None] = '26c4790c2121'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
