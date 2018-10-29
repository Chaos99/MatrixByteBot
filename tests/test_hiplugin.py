# -*- coding: utf-8 -*-
"""
Testing file for statusplugin.py
"""
from ..plugins.hiplugin import HiPlugin
from ..matrixbot import MatrixBot

class MockBot():
    """mockup class to replace bot class"""
    def __init__(self):
        self.fullname = "DummyBot"

class MockRoom():
    "mockup room"
    def __init__(self):
        self.text_response = ""

    def send_text(self, text):
        """capture the messages sent to this room"""
        self.text_response = text


def test_callback():
    """make sure some text is returned"""
    bot = MatrixBot("DummyName", "http://example.com")
    hi_plugin = HiPlugin("nametest", bot)

    events= [{'content':{'body':'!hi'}, 'sender':'test'},
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
