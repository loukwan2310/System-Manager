from project.settings.deploy import *  # noqa: F401, F403  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = True


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-erase',
    '--cover-xml-file=/tmp/coverage.xml',
    '--cover-xml',
    '--with-xunit',
    '--xunit-file=/tmp/xunittest.xml',
    '--cover-package=apps',
    '--cover-min-percentage=60',
]
