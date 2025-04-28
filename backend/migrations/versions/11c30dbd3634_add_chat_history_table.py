from alembic import op
import sqlalchemy as sa

revision = '11c30dbd3634'
down_revision = '50b6e446488c'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'chat_history',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('session_id', sa.String(length=255), nullable=False, index=True),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('chat_history')