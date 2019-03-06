import slackclient
import logging
import time
import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from settings import Setting

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class Handler:
    def __init__(self):
        st = Setting()
        self.token = st.get_token()
        self.client_id = st.get_client_id()
        self.client_secret = st.get_client_secret()
        self.bot_id = None
        self.slack_client = None
        self.chat_bot = ChatBot("Fox Bot"
                                # ,
                                # storage_adapter='chatterbot.storage.SQLStorageAdapter',
                                # logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                #                 'chatterbot.logic.BestMatch',
                                #                 'chatterbot.logic.TimeLogicAdapter'],
                                # database_uri='sqlite:///database.sqlite3'
                                )
        self.list_train=['Hello, how are you?',
                        'I am doing well.',
                        'That is good to hear.',
                        'Thank you']
        self.trainer = ListTrainer(self.chat_bot)

    def parse_bot_commands(self, events):
        for e in events:
            if e['type'] == 'message' and not 'subtype' in e:
                user_id, message = self.parse_direct_mention(e['text'])
                if user_id == self.bot_id:
                    return message, e['channel']
        return None, None

    def parse_direct_mention(self, message):
        matches = re.search("^<@(|[WU].+?)>(.*)", message)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self, command, channel):
        if command not in self.list_train and command != None:
            self.list_train.append(command)
        self.trainer.train(self.list_train)
        default_resp = self.chat_bot.get_response(command or '')
        self.slack_client.api_call('chat.postMessage',
                                   channel=channel,
                                   text=default_resp)

    def open_conct(self):
        self.slack_client = slackclient.SlackClient(token=self.token,
                                               client_id=self.client_id,
                                               client_secret=self.client_secret)
        is_ok = self.slack_client.api_call("users.list")
        # User BOT ID: BGQ99SNRM
        print(is_ok)
        if self.slack_client.rtm_connect(with_team_state=False):
            logger.info('Starter Bot connected and running!')
            self.bot_id = self.slack_client.api_call("auth.test")["user_id"]
            while True:
                command, channel = self.parse_bot_commands(self.slack_client.rtm_read())
                self.handle_command(command, channel);
                time.sleep(5)
        else:
            logger.info('Connection failed. Exception traceback printed above.')

if __name__ == '__main__':
    hd = Handler()
    hd.open_conct()