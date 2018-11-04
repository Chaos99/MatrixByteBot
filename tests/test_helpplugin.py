# -*- coding: utf-8 -*-
"""
Testing file for helpplugin.py
"""
from configparser import ConfigParser

from .helpers.mockups import MockBot, MockRoom
from ..plugins.helpplugin import HelpPlugin
from ..matrixbot import MatrixBot


def test_callback():
    """make sure some text is returned"""
    config = ConfigParser(comment_prefixes=(';'), interpolation=None)
    config.read('config/config.ini')
    bot = MatrixBot(config)
    help_plugin = HelpPlugin("nametest", bot)
    bot.add_plugin(HelpPlugin("Help-Plugin", bot))

    about_event = {'content':{'body':'!about'}}
    about_event2 = {'content':{'body':'!About'}}

    help_event = {'content':{'body':'!Help'}}
    help_event2 = {'content':{'body':'!help'}}

    room = MockRoom()
    help_plugin.callback(room, about_event)
    about = help_plugin.get_about()
    assert about == room.text_response
    room.clean_buffer()
    help_plugin.callback(room, about_event2)
    assert about == room.text_response
    room.clean_buffer()

    help_plugin.callback(room, help_event)
    help_text = help_plugin.collect_help()
    assert room.text_response == help_text
    room.clean_buffer()
    help_plugin.callback(room, help_event2)
    assert room.text_response == help_text

def test_get_help():
    """make sure some text is returned"""
    bot = MockBot()
    help_plugin = HelpPlugin("nametest", bot)
    assert len(help_plugin.get_help()) > 10
    assert len(help_plugin.get_help().split('\n')) == 2

def test_collect_help():
    """make sure some text is returned"""
    config = ConfigParser(comment_prefixes=(';'), interpolation=None)
    config.read('config/config.ini')
    bot = MatrixBot(config)
    help_plugin = HelpPlugin("nametest", bot)
    bot.add_plugin(HelpPlugin("Help-Plugin", bot))
    sample = help_plugin.collect_help()
    assert len(sample) > 10
    assert len(sample.split('\n')) >= 2
    assert "Help" in sample

def test_about():
    """make sure some text is returned"""
    bot = MockBot()
    help_plugin = HelpPlugin("nametest", bot)
    about = help_plugin.get_about()
    assert len(about) > 10
    assert "github" in about
