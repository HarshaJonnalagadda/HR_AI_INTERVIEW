# In celery_app.py or a similar file

import os
from celery import Celery
from core.config import settings

# --- Celery App Initialization ---
# This creates the Celery application instance.
# The 'include' list is crucial for Celery to find tasks in your project.
#
# CRITICAL FIX: Added all modules that contain tasks, especially those used
# by Celery Beat, to the 'include' list for auto-discovery.
celery_app = Celery(
    "hr_ai_platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "services.ai_service",
        "services.outreach_service",
        "services.brightdata_service",
        "services.calendar_service",      # <-- Added for beat schedule
        "services.analytics_service",    # <-- Added for beat schedule
        "core.security"                   # <-- Added for beat schedule
    ]
)

# --- Main Celery Configuration ---
# This section applies general configurations to the Celery app.
# Your original settings were well-configured and are kept here.
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.DEFAULT_TIMEZONE,
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,         # 30 minutes
    task_soft_time_limit=25 * 60,    # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# --- Task Routing ---
# This routes tasks to specific queues, allowing you to run different
# types of workers for different tasks (e.g., a GPU worker for AI tasks).
celery_app.conf.task_routes = {
    "services.ai_service.*": {"queue": "ai_tasks"},
    "services.outreach_service.*": {"queue": "outreach_tasks"},
    "services.brightdata_service.*": {"queue": "scraping_tasks"},
}

# --- Celery Beat Periodic Task Schedule ---
# Defines a schedule for tasks that should run automatically at set intervals.
# Commented out until tasks are implemented to prevent beat startup errors
# celery_app.conf.beat_schedule = {
#     "sync-calendar-events": {
#         "task": "services.calendar_service.sync_calendar_events",
#         "schedule": 300.0,  # Every 5 minutes
#     },
#     "cleanup-expired-tokens": {
#         "task": "core.security.cleanup_expired_tokens",
#         "schedule": 3600.0,  # Every hour
#     },
#     "generate-daily-reports": {
#         "task": "services.analytics_service.generate_daily_reports",
#         "schedule": 86400.0,  # Daily at midnight UTC
#     },
# }

# Note: The `if __name__ == "__main__":` block is generally not needed
# when running Celery with the standard CLI commands, as you are doing
# in your docker-compose.yml file.
