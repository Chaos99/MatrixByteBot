# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 23:38:58 2018

@author: ssc
"""
import re, logging
hiLog = logging.getLogger('HiPluginLog')

from plugin import Plugin

class HiPlugin(Plugin):
    def __init__(self, name, bot):
        hiLog.debug("Creating HiPlugin")
        Plugin.__init__(self, name, bot)
        hiLog.debug("Adding matcher for 'Hi'")
        Plugin.addMatcher(self, re.compile("!Hi"))
        Plugin.addMatcher(self, re.compile("!Hello"))
        
    def callback(self, room, event):
     # Somebody said hi, let's say Hi back
     hiLog.debug("{} sends response".format(self.name))
     room.send_text("Hi, " + event['sender'])
     
