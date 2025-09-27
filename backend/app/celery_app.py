"""
Celery configuration for First Contact EIS background tasks
"""

import os
from celery import Celery
from celery.schedules import crontab
import logging

logger = logging.getLogger(__name__)

# Celery configuration
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379")

# Create Celery app
celery_app = Celery(
    "firstcontact_eis",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.compliance_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.analytics_tasks",
        "app.tasks.cleanup_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1 hour
    task_ignore_result=False,
    task_store_eager_result=True,
    task_always_eager=os.getenv("CELERY_ALWAYS_EAGER", "false").lower() == "true",
    task_eager_propagates=True,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    worker_send_task_events=True,
    task_send_sent_event=True,
    task_reject_on_worker_lost=True,
    task_annotations={
        "*": {"rate_limit": "10/s"},
        "app.tasks.compliance_tasks.generate_hud_report": {"rate_limit": "1/m"},
        "app.tasks.analytics_tasks.generate_analytics": {"rate_limit": "5/m"},
    }
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    "generate-daily-reports": {
        "task": "app.tasks.compliance_tasks.generate_daily_reports",
        "schedule": crontab(hour=6, minute=0),  # Daily at 6 AM
    },
    "cleanup-old-sessions": {
        "task": "app.tasks.cleanup_tasks.cleanup_old_sessions",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    "generate-weekly-analytics": {
        "task": "app.tasks.analytics_tasks.generate_weekly_analytics",
        "schedule": crontab(hour=7, minute=0, day_of_week=1),  # Monday at 7 AM
    },
    "send-appointment-reminders": {
        "task": "app.tasks.notification_tasks.send_appointment_reminders",
        "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    "update-resource-availability": {
        "task": "app.tasks.analytics_tasks.update_resource_availability",
        "schedule": crontab(minute=0),  # Every hour
    },
    "backup-database": {
        "task": "app.tasks.cleanup_tasks.backup_database",
        "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
    },
}

# Celery signal handlers
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing"""
    logger.info(f"Request: {self.request!r}")
    return "Debug task completed"

# Error handling
@celery_app.task(bind=True)
def error_handler(self, exc, task_id, args, kwargs, einfo):
    """Global error handler for Celery tasks"""
    logger.error(f"Task {self.request.id} raised exception: {exc}")
    logger.error(f"Exception info: {einfo}")

# Task monitoring
@celery_app.task
def health_check():
    """Health check task for monitoring"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "worker_count": len(celery_app.control.inspect().active())
    }

if __name__ == "__main__":
    celery_app.start()
