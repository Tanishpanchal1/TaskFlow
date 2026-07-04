"""Reusable authorization helpers."""

from app.core.constants import UserRole


def is_admin(user) -> bool:
    role = getattr(user, "role", None)
    return getattr(role, "value", role) == UserRole.ADMIN.value


def is_team_member(user, team) -> bool:
    return is_admin(user) or user in getattr(team, "members", [])


def is_project_member(user, project) -> bool:
    team = getattr(project, "team", None)
    return team is not None and is_team_member(user, team)


def is_task_owner_or_admin(user, task) -> bool:
    return is_admin(user) or getattr(task, "assigned_to_id", None) == getattr(user, "id", None)
