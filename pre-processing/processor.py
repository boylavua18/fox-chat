import nltk
import numpy as np
import random
import string


class Processor(object):
    def __init__(self):
        nltk.download('punkt')
        nltk.download('wordnet')

    def greeting(self, message):
        f = open('../data/inputs/greetings', 'r')
        GREETINGS_INPUTS = f.read().splitlines()
        for word in message.split():
            if word.lower() in GREETINGS_INPUTS:
                f = open('../data/responses/greetings', 'r')
                GREETING_RESPONSES = f.read().splitlines()
                return random.choice(GREETING_RESPONSES)
        return None

    def response(self, user_response):
        bot_response = ''
