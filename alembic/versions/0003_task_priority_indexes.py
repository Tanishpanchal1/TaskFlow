"""task priority indexes

Revision ID: 0003_task_priority_indexes
Revises: 0002_add_comments
Create Date: 2026-07-04 00:00:00
"""

from alembic import op


revision = "0003_task_priority_indexes"
down_revision = "0002_add_comments"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_tasks_priority", "tasks", ["priority"])


def downgrade() -> None:
    op.drop_index("ix_tasks_priority", table_name="tasks")