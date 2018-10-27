# -*- coding: utf-8 -*-
"""
Testing file for helpplugin.py
"""
from ..plugins.helpplugin import HelpPlugin

class MockBot():
    def __init__(self):
        self.fullname = "DummyBot"
        
        
def test_callback():
    bot = MockBot()
    hp = HelpPlugin("nametest", bot)
    assert len(hp.get_help()) > 10
    assert len(hp.get_help().split('\n')) == 2


