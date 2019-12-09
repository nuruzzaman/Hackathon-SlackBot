import os

# https://{$YOUR_TEAM}.slack.com/apps/manage/custom-integrations
# Integration Settings API Token
SLACK_TOKEN = ''

# number of workers
MAX_WORKERS = 100

# number of redis pool
MAX_CONNECTION = 100

# set redis url if you want to enable redis related functions like redis_brain
REDIS_URL = None    # localhost
REDIS_PORT = 6379    # 6379

# command prefix
CMD_PREFIX = '!'
CMD_LENGTH = len(CMD_PREFIX)

# add your app name to this list
APPS = ['helper', 'send_email', 'noinoffice']

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
