# -*- coding: utf-8 -*-
"""
Example plugin that just says "Hi"
"""
import re
import logging
from plugin import Plugin

HI_LOG = logging.getLogger('HiPluginLog')

class HiPlugin(Plugin):
    """ Plugin that says 'Hi' if greeted"""
    def __init__(self, name, bot):
        HI_LOG.debug("Creating HiPlugin")
        Plugin.__init__(self, name, bot)
        HI_LOG.debug("Adding matcher for 'Hi'")
        Plugin.add_matcher(self, re.compile("![Hh]i"))
        Plugin.add_matcher(self, re.compile("![Hh]ello"))

    def callback(self, room, event):
        """ Return "Hi <username>" if called"""
        # Somebody said hi, let's say Hi back
        HI_LOG.debug("%s sends response", self.name)
        room.send_text("Hi, " + event['sender'])

    def get_help(self):
        """Return help text"""
        return "Answers friendly on anything starting with !Hi or !Hello"
