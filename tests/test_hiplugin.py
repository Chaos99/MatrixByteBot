# -*- coding: utf-8 -*-
"""
Testing file for statusplugin.py
"""
from configparser import ConfigParser
from .helpers.mockups import MockRoom, MockBot
from ..plugins.hiplugin import HiPlugin
from ..matrixbot import MatrixBot

def test_callback():
    """make sure some text is returned"""
    config = ConfigParser(comment_prefixes=(';'), interpolation=None)
    config.read('config/config.ini')
    bot = MatrixBot(config)
    hi_plugin = HiPlugin("nametest", bot)

    events = [{'content':{'body':'!hi'}, 'sender':'test'},
              {'content':{'body':'!Hi'}, 'sender':'test'},
              {'content':{'body':'!Hello'}, 'sender':'test'},
              {'content':{'body':'!hello'}, 'sender':'test'}]

    room = MockRoom()
    for event in events:
        hi_plugin.callback(room, event)
        assert 'Hi, test' in room.text_response

def test_get_help():
    """make sure some text is returned"""
    bot = MockBot()
    hi_plugin = HiPlugin("nametest", bot)
    assert len(hi_plugin.get_help()) > 10
    assert len(hi_plugin.get_help().split('\n')) == 1
