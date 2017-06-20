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

from argparse import ArgumentParser
import sys
import os
import yaml

import falcon
from gunicorn.six import iteritems
from gunicorn.six.moves import _thread
import logging

from taskflowbot.core import service
from rtmbot import RtmBot

sys.path.append(os.getcwd())


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


def taskflow(args=None):
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(
        logging.WARNING)
    app = falcon.API(request_type=falcon.Request)
    # if not service.initialized():
    #     service.init()
    if not args:
        args = parse_args()

    config = yaml.load(open(args.config or 'rtmbot.conf', 'r'))
    bot = RtmBot(config)
    try:
        _thread.start_new_thread(bot.start, tuple())
    except KeyboardInterrupt:
        sys.exit(0)
    return app


def start_gunicorn_server():
    """Starts server using gunicorn server.
    """
    from gunicorn.app.base import Application

    class WSGIServer(Application):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super(WSGIServer, self).__init__()

        def load_config(self):
            config = dict(
                [(key, value) for key, value in iteritems(self.options)
                 if key in self.cfg.settings and value is not None])
            for key, value in iteritems(config):
                self.cfg.set(key.lower(), value)

        def load(self):
            return taskflow()

    options = {
        'bind': '%s:%s' % ('0.0.0.0', os.environ['PORT']),
        'workers': 2,
        'loglevel': 'DEBUG',
        'worker_class': 'gthread'
    }

    WSGIServer(taskflow(), options).run()

if __name__ == '__main__':
    start_gunicorn_server()
