import os
from dotenv import load_dotenv
from pathlib import Path

class Setting:
    def __init__(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

    def get_token(self):
        return os.getenv("FOX_SLACK_TOKEN")

    def get_app_name(self):
        return os.getenv("FOX_SLACK_NAME")

    def get_client_id(self):
        return os.getenv("CLIENT_ID")

    def get_client_secret(self):
        return os.getenv("CLIENT_SECRET")

    def get_bot_id(self):
        return os.getenv("BOT_ID")