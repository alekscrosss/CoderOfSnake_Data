"""remove user_id column

Revision ID: e4d2c470fcde
Revises: fa3401d90b43
Create Date: 2024-06-16 11:42:49.569993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4d2c470fcde'
down_revision: Union[str, None] = 'fa3401d90b43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
