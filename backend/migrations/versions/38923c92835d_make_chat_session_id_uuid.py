"""Make chat_session.id UUID

Revision ID: 38923c92835d
Revises: 06cdf0d75f68
Create Date: 2025-04-27 17:55:45.310380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38923c92835d'
down_revision = '06cdf0d75f68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
