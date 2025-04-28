"""Make chat_session.id UUID

Revision ID: 06cdf0d75f68
Revises: 4bd521599a09
Create Date: 2025-04-27 17:52:51.105924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06cdf0d75f68'
down_revision = '4bd521599a09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
