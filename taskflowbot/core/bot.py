import os

from slackbot.bot import Bot as BaseBot
from slackbot import settings

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_VERIFICATION_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']


class Bot(BaseBot):
    
    def __init__(self):
        settings.API_TOKEN = SLACK_BOT_TOKEN
        super(Bot, self).__init__()
