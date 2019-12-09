import os
import sys
sys.path.append(os.path.abspath('.'))

import time
import traceback
from importlib import import_module
from slackclient import SlackClient
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from brain import RedisBrain
from loggers import logger, level
from settings import APPS, CMD_PREFIX, CMD_LENGTH, SLACK_TOKEN, MAX_WORKERS

#chatbot
from chatbot.chatbot import ChatBot

class Robot(object):

    def __init__(self):
        self.client = SlackClient(SLACK_TOKEN)
        self.brain = RedisBrain()
        self.apps, self.docs = self.load_apps()
        self.logger = logger

    def load_apps(self):
        docs = ['='*14, 'Usage', '='*14]
        apps = {}

        for name in APPS:
            app = import_module('apps.%s' % name)
            docs.append('{0}{1}: {2}'.format(
                CMD_PREFIX, ', '.join(app.run.commands), app.run.__doc__
            ))
            for command in app.run.commands:
                apps[command] = app

        return apps, docs

    def handle_message(self, message):
        channel, user, text = message

        #convert into UPPERCASE
        text = text.upper()

        command, payloads = self.extract_command(text)
        app = self.apps.get(command, None)

        # Fetch your Bot's User ID
        # PUT BOT'S NAME
        # user_list = self.client.api_call("users.list")
        # for user in user_list.get('members'):
        #     if user.get('name') == "hackathon-bot":
        #         slackbot_id = user.get('id')
        #         print("my bot id: ", slackbot_id)
        #         break


        if not command:
            aichatbot_gen_mgs = bot.response(text)
            self.client.api_call("chat.postMessage",channel=channel,text=aichatbot_gen_mgs)
            return

        if not app:
            return

        try:
            app.run(self, channel, user, payloads)
        except:
            self.logger.error(traceback.format_exc())


    def extract_messages(self, events):
        messages = []
        for event in events:
            channel = event.get('channel', '')
            user = event.get('user', '')
            text = event.get('text', '')
            if channel and user and text:
                messages.append((channel, user, text))
        return messages


    def extract_command(self, text):
        if CMD_PREFIX and CMD_PREFIX != text[0]:
            return (None, None)

        tokens = text.split(' ', 1)
        if 1 < len(tokens):
            return tokens[0][CMD_LENGTH:], tokens[1]
        else:
            return (text[CMD_LENGTH:], '')

    def rtm_connect(self):
        while not self.client.rtm_connect(with_team_state=False):
            self.logger.info('RTM Connecting...')
            time.sleep(1)
        self.logger.info('RTM Connected.')

    def read_message(self):
        try:
            return self.client.rtm_read()
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            self.logger.error(traceback.format_exc())
            self.rtm_connect()

    def run(self):
        self.brain.connect()
        self.rtm_connect()
        if not self.client.server.connected:
            raise RuntimeError(
                'Can not connect to slack client. Check your settings.'
            )

        while True:
            events = self.read_message()
            if events:
                messages = self.extract_messages(events)
                if messages:
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        try:
                            executor.map(self.handle_message, messages)
                        except TimeoutError:
                            self.logger.error(traceback.format_exc())
            else:
                time.sleep(0.3)

    def disconnect(self):
        if self.client and self.client.server and self.client.server.websocket:
            self.client.server.websocket.close()
        self.logger.info('RTM disconnected.')

if '__main__' == __name__:

    robot = Robot()
    bot = ChatBot()
    try:
        robot.run()
    except KeyboardInterrupt as e:
        robot.logger.info('Hackathon bot Shutdown By Admin.')
    finally:
        robot.disconnect()
        robot.logger.info('Hackathon bot Shutdown.')