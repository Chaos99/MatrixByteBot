# -*- coding: utf-8 -*-
""" Main matrix bot that handles server connection, keeps plugin list
and registers them as listeners"""

import logging
from urllib.parse import urlparse
from time import sleep
from threading import Thread, Event

import schedule

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi
from matrix_client.errors import MatrixRequestError

BOT_LOG = logging.getLogger('BotLog')

class MatrixBot:
    """The main bot, connecting to the server and handling plugins"""
    def __init__(self, username, server):
        self.username = username
        self.fullname = "@"+str(username).lower()+':'+urlparse(server).hostname
        self.plugins = []
        self.api = None
        self.current_room = ""
        self.members = []
        self.all_rooms = None

        # Connect to server
        BOT_LOG.debug("creating matrix client for server %s", server)
        self.client = MatrixClient(server)


    def connect(self, username, password, server, room_id):
        ''' log in to the server and get connected rooms'''
        try:
            BOT_LOG.debug("Trying to log in as %s pw: %s",
                          username, "".join(['*' for p in password]))
            token = self.client.login(username, password)
            BOT_LOG.debug("Got Token %s..%s", token[0:3], token[-3:-1])
        except MatrixRequestError as error:
            BOT_LOG.error("Login Failed: Code: %s, Content: %s", error.code, error.content)
        #this is a second connection with different interface
        BOT_LOG.debug("Creating matrix API endpoint")
        self.api = MatrixHttpApi(server, token)
        if str(room_id).startswith('!'):
            self.current_room = room_id
        else:
            self.current_room = self.get_room_id_by_name(room_id)
        BOT_LOG.debug("Joining room with id %s", self.current_room)
        self.api.join_room(self.current_room)

        BOT_LOG.debug("Getting member info")
        self.members = self.api.get_room_members(self.current_room)
        BOT_LOG.debug("Members in room: %s",
                      ",".join([a['sender']
                                if 'sender' in a.keys() else ""
                                for a in self.members['chunk']]))
        rooms = []
        for _, room in self.client.get_rooms().items():
            rooms.append(room)

        self.all_rooms = VirtualRoom(rooms)


    def init_scheduler(self):
        ''' initialize a thread that handles the event loop for
        the scheduler for all plugins'''
        BOT_LOG.debug("Spinning up scheduler thread")
        self.schedule = schedule
        self.killswitch = Event()
        self.killswitch.clear()
        self.thread = Thread(target=self.schedule_loop, args=(self.killswitch,))
        #self.thread.daemon = True
        self.thread.start()

    def stop_scheduler(self):
        ''' wind down the scheduler thread gracefully before exit'''
        BOT_LOG.debug("Trying to end scheduler thread ..")
        self.killswitch.set()
        self.thread.join()
        BOT_LOG.debug("..successful")

    def schedule_loop(self, stop_event):
        ''' this event loop is run inside the scheduler thread'''
        BOT_LOG.debug("Scheduler thread started successfully")
        while not stop_event.is_set():
            #BOT_LOG.debug("Scheduler loop runs")
            self.schedule.run_pending()
            sleep(10)

    def add_plugin(self, plugin):
        """Puts a plugin in the internal list
        where it will be registered as a listener"""
        self.plugins.append(plugin)

    def get_room_id_by_name(self, name):
        """Translate human-readable room name into internal room id"""
        BOT_LOG.debug("Getting room ID for name '%s'", name)
        if str(name).startswith('#'):
            rid = self.api.get_room_id(name)
        else:
            rid = self.api.get_room_id('#' + name)
        if rid is None:
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

    def register_listeners(self):
        ''' register the added plugins as listeners into the rooms
        the bot si connected to'''
        rooms = []
        for room_id, room in self.client.get_rooms().items():
            BOT_LOG.debug("Registering plugins in room %s (%s)", room.name, room_id)
            rooms.append(room)
            for plugin in self.plugins:
                room.add_listener(plugin.handle_message)

class VirtualRoom:
    ''' offering matrix-client room like interfaces for a list of
    several rooms to make general anouncements'''
    def __init__(self, room_list):
        self.room_list = room_list
        self.name = None
        self.cannonical_alias = None

    def send_text(self, text):
        'send a text message to all rooms'
        for room in self.room_list:
            room.send_text(text)

    def display_name(self):
        """Calculates the display name for a room."""
        self.name = "\n".join([room.name for room in self.room_list])
        if len(self.name) < 2:
            self.name = "{} unnamed rooms".format(len(self.room_list))
        return self.name
