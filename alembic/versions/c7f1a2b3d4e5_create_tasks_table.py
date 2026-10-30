"""create tasks table

Revision ID: c7f1a2b3d4e5
Revises: 9b2d7f1a4c30
Create Date: 2026-10-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c7f1a2b3d4e5"
down_revision: Union[str, Sequence[str], None] = "9b2d7f1a4c30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


task_status = sa.Enum(
    "PENDING",
    "INPROGRESS",
    "COMPLETED",
    name="task_status",
    create_type=False,
)
task_priority = sa.Enum(
    "LOW",
    "MEDIUM",
    "HIGH",
    name="task_priority",
    create_type=False,
)


def upgrade() -> None:
    task_status.create(op.get_bind(), checkfirst=True)
    task_priority.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            task_status,
            server_default=sa.text("'PENDING'"),
            nullable=False,
        ),
        sa.Column(
            "priority",
            task_priority,
            server_default=sa.text("'MEDIUM'"),
            nullable=False,
        ),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    task_priority.drop(op.get_bind(), checkfirst=True)
    task_status.drop(op.get_bind(), checkfirst=True)
