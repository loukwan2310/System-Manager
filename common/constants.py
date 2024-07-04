FITBIT_API_URL = 'https://api.fitbit.com'
FITBIT_RESPONSE_TYPE = 'code'
FITBIT_CHALLENGE_METHOD = 'S256'
FITBIT_SCOPE = 'activity heartrate location nutrition oxygen_saturation ' \
               'profile respiratory_rate settings sleep social temperature weight'
FITBIT_DEFAULT_DETAIL_LEVEL = '1min'
FITBIT_DEFAULT_START_TIME = '00:00'
FITBIT_DEFAULT_END_TIME = '23:59'
FITBIT_DEFAULT_ACCEPT_LOCALE = 'en_GB'
FITBIT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

WEEKDAY_NUMBERS = {
    'MONDAY': 0,
    'TUESDAY': 1,
    'WEDNESDAY': 2,
    'THURSDAY': 3,
    'FRIDAY': 4,
    'SATURDAY': 5,
    'SUNDAY': 6
}

MAXIMUM_RANDOM_NUMBER = 9999

NOT_EQUAL_OPERATOR = '!='

ORM_OPERATORS = {
    '=': '',
    '>': '__gt',
    '>=': '__gte',
    '<': '__lt',
    '<=': '__lte',
}
