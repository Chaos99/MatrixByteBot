# -*- coding: utf-8 -*-
"""
helper classes for testing;
mock objects to replace existing classes
"""
from configparser import ConfigParser
import schedule
import logging

MOCK_LOG = logging.getLogger('MockLog')

class MockBot():
    """mockup class to replace bot class"""
    def __init__(self, config = ''):
        self.fullname = "DummyBot"
        self.schedule = schedule
        config = ConfigParser(comment_prefixes=(';'), interpolation=None)
        config.read('config/config.ini')
        self.config = config
        self.schedule = schedule
        self.all_rooms = MockRoom("Bytespeicher")


class MockRoom():
    "mockup room"
    def __init__(self, name=''):
        self.text_response = ""
        self.name = name
        self.first_response = True
        self.all_rooms = None

    def send_text(self, text):
        """capture the messages sent to this room"""
        MOCK_LOG.debug("Sending text '%s' to mock room for test", text)
        if self.first_response:
            self.text_response += text
            self.first_response = False
        else:
            self.text_response += ('\n') + text

    def clean_buffer(self):
        '''clear the message buffer'''
        self.text_response = ''
        self.first_response = True

    def copy(self):
        return MockRoom(self.name)
