# -*- coding: utf-8 -*-
"""
Testing file for statusplugin.py
"""
from configparser import ConfigParser
from unittest import mock

from .helpers.mockups import MockRoom, MockBot

from ..plugins.statusplugin import StatusPlugin
from ..matrixbot import MatrixBot

def test_callback():
    """make sure some text is returned"""

    config = ConfigParser(comment_prefixes=(';'))
    config.read('config/config.ini')
    bot = MockBot()
    status_plugin = StatusPlugin("nametest", bot)

    users_event = {'content':{'body':'!users'}}
    users_event2 = {'content':{'body':'!Users'}}

    status_event = {'content':{'body':'!Status'}}
    status_event2 = {'content':{'body':'!status'}}

    room = MockRoom()
    status_plugin.users(room)
    call = room.text_response
    room.clean_buffer()
    status_plugin.callback(room, users_event)
    assert room.text_response == call
    room.clean_buffer()
    status_plugin.callback(room, users_event2)
    assert room.text_response == call
    room.clean_buffer()

    status_plugin.status(room)
    call = room.text_response
    room.clean_buffer()
    status_plugin.callback(room, status_event)
    assert room.text_response == call
    room.clean_buffer()
    status_plugin.callback(room, status_event2)
    assert room.text_response == call

def test_get_help():
    """make sure some text is returned"""
    bot = MockBot()
    status_plugin = StatusPlugin("nametest", bot)
    assert len(status_plugin.get_help()) > 10
    assert len(status_plugin.get_help().split('\n')) == 2

def test_spaceapi():
    """make sure some text is returned"""
    config = ConfigParser(comment_prefixes=(';'), interpolation=None)
    config.read('config/config.ini')
    bot = MockBot()
    #bot = MatrixBot(config)
    #bot.init_scheduler()
    status_plugin = StatusPlugin("nametest", bot)
    room = MockRoom()
    sample = status_plugin.spaceapi(room)
    assert sample['space'] == 'Bytespeicher'
    #bot.stop_scheduler()

def test_users():
    """make sure some text is returned"""
    config = ConfigParser(comment_prefixes=(';'), interpolation=None)
    config.read('config/config.ini')
    bot = MockBot()
    #bot = MatrixBot(config)
    #bot.init_scheduler()
    status_plugin = StatusPlugin("nametest", bot)
    room = MockRoom()
    status_plugin.users(room)
    assert "space" in room.text_response or "Space" in room.text_response
    #bot.stop_scheduler()

def test_status():
    """make sure some text is returned"""
    config = ConfigParser(comment_prefixes=(';'), interpolation=None)
    config.read('config/config.ini')
    #bot = MatrixBot(config)
    bot = MockBot()
    #bot.init_scheduler()
    status_plugin = StatusPlugin("nametest", bot)
    room = MockRoom()
    status_plugin.status(room)
    assert "open" in room.text_response or "closed" in room.text_response
    #bot.stop_scheduler()

def test_status_announce_change():
    """make sure some text is returned"""
    config = ConfigParser(comment_prefixes=(';'), interpolation=None)
    config.read('config/config.ini')
    bot = MockBot()
    bot.all_rooms = MockRoom("Bytespeicher")
    status_plugin = StatusPlugin("nametest", bot)
    # output status on first start
    with mock.patch.object(StatusPlugin, 'spaceapi', return_value={"space":"Bytespeicher", "state" : { "open" : False}}):
        status_plugin.status_announce_change()
        assert "open" in bot.all_rooms.text_response or "closed" in bot.all_rooms.text_response
    bot.all_rooms.clean_buffer()
    # no output without change of state
    with mock.patch.object(StatusPlugin, 'spaceapi', return_value={"space":"Bytespeicher", "state" : { "open" : False}}):
        status_plugin.status_announce_change()
        assert bot.all_rooms.text_response == ""
    # trigger output with change
    with mock.patch.object(StatusPlugin, 'spaceapi', return_value={"space":"Bytespeicher", "state" : { "open" : True}}):
        status_plugin.status_announce_change()
        assert "open" in bot.all_rooms.text_response