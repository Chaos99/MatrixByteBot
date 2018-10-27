# -*- coding: utf-8 -*-
"""
Testing file for helpplugin.py
"""
from ..plugins.helpplugin import HelpPlugin
from ..matrixbot import MatrixBot

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

def test_collect_help():
    """make sure some text is returned"""
    bot = MatrixBot("DummyName", "http://example.com")
    help_plugin = HelpPlugin("nametest", bot)
    bot.add_plugin(HelpPlugin("Help-Plugin", bot))
    sample = help_plugin.collect_help()
    assert len(sample) > 10
    assert len(sample.split('\n')) >= 2
    assert "Help" in sample
