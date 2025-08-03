"""rename avartar to avatar

Revision ID: 6dd4dfd674c0
Revises: f29461450e01
Create Date: 2025-08-03 15:56:37.502260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dd4dfd674c0'
down_revision: Union[str, None] = 'f29461450e01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table('avartar', 'avatar')

def downgrade():
    op.rename_table('avatar', 'avartar')
