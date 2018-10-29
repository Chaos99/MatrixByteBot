# -*- coding: utf-8 -*-
"""
Testing file for helpplugin.py
"""
from ..plugins.maintenanceplugin import MaintenancePlugin

class MockBot():
    """mockup class to replace bot class"""
    def __init__(self):
        self.fullname = "DummyBot"

def test_get_version():
    """make sure some text is returned"""
    bot = MockBot()
    mtn_plugin = MaintenancePlugin("nametest", bot)
    version = mtn_plugin.get_version()
    assert len(version) == 5
    assert len(version.split('.')) == 3

def test_get_uptime():
    """make sure some text is returned"""
    bot = MockBot()
    mtn_plugin = MaintenancePlugin("nametest", bot)
    assert len(mtn_plugin.get_uptime()) >= 7
    assert len(mtn_plugin.get_uptime().split(':')) >= 3

def test_get_history():
    """make sure some text is returned"""
    bot = MockBot()
    mtn_plugin = MaintenancePlugin("nametest", bot)
    history = mtn_plugin.get_history()
    assert len(history.split('\n')) >= 5
    version = mtn_plugin.get_version()
    assert version in history
