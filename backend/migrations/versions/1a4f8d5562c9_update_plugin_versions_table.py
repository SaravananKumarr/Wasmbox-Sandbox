"""update plugin_versions table

Revision ID: 1a4f8d5562c9
Revises: 17fd4231d59d
Create Date: 2026-07-25 13:44:37.955290
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1a4f8d5562c9"
down_revision: Union[str, Sequence[str], None] = "17fd4231d59d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "plugin_versions",
        sa.Column(
            "title",
            sa.String(length=150),
            nullable=True,
        ),
    )

    op.add_column(
        "plugin_versions",
        sa.Column(
            "changelog",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "plugin_versions",
        sa.Column(
            "release_notes",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "plugin_versions",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="stable",
        ),
    )

    op.add_column(
        "plugin_versions",
        sa.Column(
            "is_latest",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.add_column(
        "plugin_versions",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.alter_column(
        "plugin_versions",
        "version",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=20),
        existing_nullable=False,
        postgresql_using="version::text",
    )

    op.create_index(
        "ix_plugin_versions_plugin_id",
        "plugin_versions",
        ["plugin_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_plugin_versions_plugin_id",
        table_name="plugin_versions",
    )

    op.alter_column(
        "plugin_versions",
        "version",
        existing_type=sa.String(length=20),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="version::integer",
    )

    op.drop_column("plugin_versions", "updated_at")
    op.drop_column("plugin_versions", "is_latest")
    op.drop_column("plugin_versions", "status")
    op.drop_column("plugin_versions", "release_notes")
    op.drop_column("plugin_versions", "changelog")
    op.drop_column("plugin_versions", "title")