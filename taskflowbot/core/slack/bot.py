# Copyright 2017 Hieu LE
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from slackbot.bot import Bot as BaseBot
from slackbot import settings

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_VERIFICATION_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']


class Bot(BaseBot):
    
    def __init__(self):
        settings.API_TOKEN = SLACK_BOT_TOKEN
        super(Bot, self).__init__()
