from celery.schedules import crontab


CELERY_IMPORTS = ('app.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'celery-event': {
        'task': 'app.tasks.periodic_run',
        'schedule': crontab(minute="*/60"),
    }
}
