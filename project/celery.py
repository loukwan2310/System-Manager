# from celery import Celery
# from celery.schedules import crontab
#
# app = Celery('project')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
#
# app.conf.beat_schedule = {
#     'sync-mission-completed-of-users-yesterday-task': {
#         'task': 'apps.users.tasks.sync_mission_completed_of_users_yesterday_task',
#         'schedule': crontab(hour=0, minute=0)
#     },
#     'update-training-level-of-the-user-task': {
#         'task': 'apps.users.tasks.update_training_level_of_the_user_task',
#         'schedule': crontab(hour=0, minute=0, day_of_week="mon")
#     },
#     'sync-data-from-fitbit-task': {
#         'task': 'apps.users.tasks.sync_data_from_the_fitbit_task',
#         'schedule': crontab(minute='*/10')
#     },
#     'send-notification-to-the-users-task': {
#         'task': 'apps.notifications.tasks.send_notification_to_the_users_task',
#         'schedule': crontab(minute='*/10')
#     }
# }
