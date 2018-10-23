# -*- coding: utf-8 -*-
""" Main matrix bot that handles server connection, keeps plugin list
and registers them as listeners"""

import logging
from urllib.parse import urlparse

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi

BOT_LOG = logging.getLogger('BotLog')

class MatrixBot:
    """The main bot, connecting to the server and handling plugins"""
    def __init__(self, username, password, server, roomId):
        self.username = username
        self.fullname = "@"+str(username).lower()+':'+urlparse(server).hostname
        self.plugins = []
        # Connect to server
        BOT_LOG.debug("creating matrix client for server %s", server)
        self.client = MatrixClient(server)
        try:
            BOT_LOG.debug("Trying to log in as %s pw: %s",
                          username, "".join(['*' for p in password]))
            self.token = self.client.login_with_password(username, password)
            BOT_LOG.debug("Got Token %s..%s", self.token[0:3], self.token[-3:-1])
        except Exception as e:
            BOT_LOG.error("Login Failed: %s", e)
            return None
        #this is a second connection with different interface
        BOT_LOG.debug("Creating matrix API endpoint")
        self.api = MatrixHttpApi(server, self.token)
        BOT_LOG.debug("Syncing..")
        self.api.sync()
        if str(roomId).startswith('!'):
            self.current_room = roomId
        else:
            self.current_room = self.get_room_id_by_name(roomId)
        BOT_LOG.debug("Joining room with id %s", self.current_room)
        self.api.join_room(self.current_room)

        BOT_LOG.debug("Getting member info")
        self.members = self.api.get_room_members(self.current_room)
        BOT_LOG.debug("Members in room: %s",
                      ",".join([a['sender']
                                if 'sender' in a.keys() else ""
                                for a in self.members['chunk']]))
        #self.rooms =
        return None

    def add_plugin(self, plugin):
        """Puts a plugin in the internal list
        where it will be registered as a listener"""
        self.plugins.append(plugin)

    def get_room_id_by_name(self, name):
        """Translate human-readable room name into internal room id"""
        BOT_LOG.debug("Getting room ID for name '%s'", name)
        try:
            if str(name).startswith('#'):
                rid = self.api.get_room_id(name)
            else:
                rid = self.api.get_room_id('#' + name)
        except Exception:
            BOT_LOG.warning("Room name '%s' not found", name)
            rid = ""
        return rid

    def send(self, text):
        """Sending initial message to room to announce startup"""
        BOT_LOG.debug("Sending sample text to room")
        self.api.send_message(self.current_room, text)

    def start_polling(self):
        """Starts syncing and polling for new messages in a new thread"""
        # Starts polling for messages
        self.client.start_listener_thread()
        return self.client.sync_thread
