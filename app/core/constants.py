"""
Application-wide constants.

Avoid magic strings throughout the project by importing
values from this module.
"""

from enum import Enum

# ------------------------------------------------------------------
# API
# ------------------------------------------------------------------

API_V1_PREFIX = "/api/v1"

# ------------------------------------------------------------------
# Pagination
# ------------------------------------------------------------------

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ------------------------------------------------------------------
# JWT
# ------------------------------------------------------------------

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

# ------------------------------------------------------------------
# User Roles
# ------------------------------------------------------------------


class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"


# ------------------------------------------------------------------
# Task Status
# ------------------------------------------------------------------


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


# ------------------------------------------------------------------
# Task Priority
# ------------------------------------------------------------------


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"