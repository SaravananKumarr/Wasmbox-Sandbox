"""create execution_logs table

Revision ID: 0a2fef6d2611
Revises: d136b503d490
Create Date: 2026-08-03 00:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0a2fef6d2611'
down_revision: Union[str, Sequence[str], None] = 'd136b503d490'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'execution_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('plugin_id', sa.String(), nullable=True),
        sa.Column('plugin_name', sa.String(length=255), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('input_payload', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('return_code', sa.Integer(), nullable=False),
        sa.Column('duration_ms', sa.Float(), nullable=False),
        sa.Column('memory_mb', sa.Float(), nullable=False),
        sa.Column('output', sa.Text(), nullable=True),
        sa.Column('logs', sa.JSON(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['plugin_id'], ['plugins.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_execution_logs_plugin_id'), 'execution_logs', ['plugin_id'], unique=False)
    op.create_index(op.f('ix_execution_logs_created_at'), 'execution_logs', ['created_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_execution_logs_created_at'), table_name='execution_logs')
    op.drop_index(op.f('ix_execution_logs_plugin_id'), table_name='execution_logs')
    op.drop_table('execution_logs')
