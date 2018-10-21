# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 23:13:53 2018

@author: ssc
"""
import logging, re, traceback
pluginLog = logging.getLogger('PluginLog')

class Plugin:
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
        self.rooms = []
        self.matchers = []
        pluginLog.debug("Loading Plugin {}".format(name))
        pluginLog.debug("Set up filtering for {}".format(self.bot.fullname))
        
    def addMatcher(self, compiledRe):
        pluginLog.debug("Adding RegEx {} to {}".format(compiledRe, self.name))
        self.matchers.append(compiledRe)

    def handle_message(self, room, event):
        # Make sure we didn't send this message
        try:
            pluginLog.debug("Handling message {}:{}".format(event['sender'], event['content']['body']))
        except Exception as e:
            pluginLog.debug("Message {} caused exception {}".format(event, e))
        if re.match(self.bot.fullname, event['sender']):
            pluginLog.debug("Discarded because self-sent")
            return

        # Loop through all installed handlers and see if they need to be called
        if event['type'] == "m.room.message":
            for matcher in self.matchers:
                if matcher.match(event['content']['body']):
                    # This handler needs to be called
                    pluginLog.debug("Match found with {}".format(matcher))
                    try:
                        self.callback(room, event)
                    except:
                        traceback.print_exc()
        else:
            pluginLog.debug("Discarded because not room message")

    def handle_invite(self, room_id, state):
        pluginLog.debug("Got invite to room: {}".format(room_id))
        pluginLog.debug("Joining...")
        room = self.bot.client.join_room(room_id)

        # Add message callback for this room
        room.add_listener(self.handle_message)

        # Add room to list
        self.rooms.append(room)

    def start_polling(self):
        # Starts polling for messages
        pluginLog.debug("{} starts polling".format(self.name))
        self.bot.client.start_listener_thread()
        return self.bot.client.sync_thread
    
    def callback(self):
        raise NotImplementedError('You need to define a "callback()" method!')
