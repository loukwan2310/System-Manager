from enum import Enum


class EvaluationType(Enum):
    TOTAL_EXERCISE_TIME = 1
    LONGEST_CONTINUOUS_EXERCISE_TIME = 2
    NUMBER_OF_MISSION_COMPLETED = 3


class CalculateEvaluation(Enum):
    FIRST_OF_WEEK = 2
    SECOND_OF_WEEK = 4


class EvaluationStatus(Enum):
    """
        Enum: Evaluation Status

        TOTAL_ETL:  Total exercise time lowest
        TOTAL_ETH: Total exercise time highest
        LONGEST_CONTINUOUS_ETL:  longest continuous exercise time lowest
        LONGEST_CONTINUOUS_HIGHEST: longest continuous exercise time highest
    """
    DEFAULT = 0
    TOTAL_ETL = 1
    LONGEST_CONTINUOUS_ETL = 2
    MISSION_COMPLETED_LOWEST = 3
    MISSION_COMPLETED_HIGHEST = 4
    LONGEST_CONTINUOUS_HIGHEST = 5
    TOTAL_ETH = 6
    EQUALS_ALL = 7


class CompareCDST(Enum):
    """
        Enum: Compare current date vs start date
    """

    EQUAL = 0
    GT_ONE_DAY = 1
    GTE_SECOND_DAY = 2


class MissionDateRange(Enum):
    TODAY = 'today'
    CURRENT_WEEK = 'current_week'

    @classmethod
    def items(cls):
        return [(item.value, item.name) for item in cls]


class UserMissionStatus(Enum):
    CHALLENGING = 1
    COMPLETED = 2

    @classmethod
    def items(cls):
        return [(item.value, item.name) for item in cls]


class NotificationCriteriaFieldName(Enum):
    DAILY_MISSION_STATUS = 'daily_mission_status'
    UNNOTIFIED_EXERCISE_HISTORY_NUMBER = 'unnotified_exercise_history_numbers'
    TIME_FROM_LATEST_EXERCISE = 'time_from_latest_exercise'
    OVERALL_EVALUATION = 'overall_evaluation'
    OVER_EVALUATION_B = 'overall_evaluation_b'
    EVALUATION_STATUS = 'evaluation_status'
    IS_WORKING_DAY = 'is_working_day'


class NotificationType(Enum):
    NO_ACTION = 0
    MISSION_COMPLETED = 1
    HOME_PAGE_HEART_RATE = 2
    MISSION_SELECTION = 3
    DATE_EXERCISE_HISTORY = 4


class DailyMissionStatus(Enum):
    CHALLENGING = 1
    COMPLETED = 2
    UNNOTIFIED_CHALLENGING = 3
    UNNOTIFIED_COMPLETED = 4
    HAVE_NOT_ACCEPT = 5


class FirebaseMessageType(Enum):
    NOTIFICATION_MESSAGE = 1
    DATA_MESSAGE = 2


class NotificationAction(Enum):
    RESTING_HEAT_RATE_MEASUREMENT = 'RESTING_HEAT_RATE_MEASUREMENT'
    ENFORCE_STOP_EXERCISE = 'ENFORCE_STOP_EXERCISE'
