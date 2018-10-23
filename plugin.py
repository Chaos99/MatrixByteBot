# -*- coding: utf-8 -*-
"""
Virtual base class for all plugins.
Handles regex and checking incomming messages for matches
"""
import logging
import re
import traceback

PLUGIN_LOG = logging.getLogger('PluginLog')

class Plugin:
    """(Virtual) base class for Plugins"""
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
        self.rooms = []
        self.matchers = []
        PLUGIN_LOG.debug("Loading Plugin %s", name)
        PLUGIN_LOG.debug("Set up filtering for %s", self.bot.fullname)

    def add_matcher(self, compiled_re):
        """Add a (compiled) regular expression
        for which the plugin should listen"""

        PLUGIN_LOG.debug("Adding RegEx %s to %s", compiled_re, self.name)
        self.matchers.append(compiled_re)

    def handle_message(self, room, event):
        """Parses incomming messages, matches with regex and decides
        if callback is called"""

        # Make sure we didn't send this message
        try:
            PLUGIN_LOG.debug("Handling message %s:%s", event['sender'], event['content']['body'])
        except Exception as e:
            PLUGIN_LOG.debug("Message %s caused exception %s", event, e)
        if re.match(self.bot.fullname, event['sender']):
            PLUGIN_LOG.debug("Discarded because self-sent")
            return

        # Loop through all installed handlers and see if they need to be called
        if event['type'] == "m.room.message":
            for matcher in self.matchers:
                if matcher.match(event['content']['body']):
                    # This handler needs to be called
                    PLUGIN_LOG.debug("Match found with %s", matcher)
                    try:
                        self.callback(room, event)
                    except Exception:
                        traceback.print_exc()
        else:
            PLUGIN_LOG.debug("Discarded because not room message")

    def callback(self, room, event):
        """ Pure Virtual: Overwrite with callback (e.g. what to do)"""
        raise NotImplementedError('You need to define a "callback()" method!')

    def get_help(self):
        """ Pure Virtual: return help text string for plugin"""
        raise NotImplementedError('You need to define a "getHelp()" method!')
