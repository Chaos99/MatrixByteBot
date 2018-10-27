# -*- coding: utf-8 -*-
"""
Testing file for helpplugin.py
"""
from ..plugins.helpplugin import HelpPlugin

class MockBot():
    """mockup class to replace bot class"""
    def __init__(self):
        self.fullname = "DummyBot"

def test_callback():
    """make sure some text is returned"""
    bot = MockBot()
    help_plugin = HelpPlugin("nametest", bot)
    assert len(help_plugin.get_help()) > 10
    assert len(help_plugin.get_help().split('\n')) == 2


