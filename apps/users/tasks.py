import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.users.models import User, FitbitUser, SystemSetting
from common.fitbit_client import FitbitClient

logger = logging.getLogger(__file__)


@shared_task
def update_training_level_of_the_user_task():
    """
    Update training level of the user task
    """
    users = User.objects.select_related('training_level').all()
    for user in users:
        user.update_training_level_of_the_user()


@shared_task
def sync_data_from_the_fitbit_task():
    """
    Sync data from the fitbit task
    """
    fitbit_client = FitbitClient()
    current_time = timezone.localtime(timezone.now())

    system_setting = SystemSetting.objects.order_by('-created_at').first()
    fitbit_users = FitbitUser.objects.select_related('target_user').all()
    for fitbit_user in fitbit_users:
        fitbit_user.sync_user_profile_from_fitbit(fitbit_client)
        fitbit_user.sync_heart_rate_intraday_from_fitbit(fitbit_client)
        fitbit_user.sync_mission_completed_from_fitbit(fitbit_client, current_time)
        fitbit_user.sync_relevant_data_from_heart_rate_intraday(fitbit_client, system_setting, current_time)


@shared_task
def sync_mission_completed_of_users_yesterday_task():
    """
    Sync mission completed of user yesterday task
    """
    fitbit_client = FitbitClient()
    current_time = timezone.localtime(timezone.now())
    yesterday = current_time - timedelta(days=1)
    fitbit_users = FitbitUser.objects.select_related('target_user').all()
    for fitbit_user in fitbit_users:
        fitbit_user.sync_mission_completed_from_fitbit(fitbit_client, yesterday)
