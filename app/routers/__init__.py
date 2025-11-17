# app/routers/__init__.py

from .auth import router as auth_router
from .me import router as me_router
from .scholarship_types import router as scholarship_types_router
from .scholarship_periods import router as scholarship_periods_router
from .requirements import router as requirements_router
from .applications import router as applications_router
from .student_applications import router as student_applications_router
from .documents import router as documents_router
from .application_status import router as application_status_router
from .status_history import router as status_history_router
from .review_queue import router as review_queue_router
from .decisions import router as decisions_router
from .announcements import router as announcements_router
from .notifications import router as notifications_router
from .dashboard import router as dashboard_router
