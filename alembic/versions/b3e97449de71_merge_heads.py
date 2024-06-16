"""merge heads

Revision ID: b3e97449de71
Revises: 4544ab395a6b, c86f63425988
Create Date: 2024-06-14 23:45:11.424266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3e97449de71'
down_revision: Union[str, None] = ('4544ab395a6b', 'c86f63425988')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
