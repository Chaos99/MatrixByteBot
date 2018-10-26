# MatrixByteBot
## Description
 A bot living in the channels of the Erfurt Hackspace 'Bytespeicher' or the Makerspace,
 serving its users.

 Interfacing a matrix network, using the matrix-sdk.
 Written in Python 3.6.

## Status
~~Concept phase and build environment setup~~  
~~Prototyping login and triggering~~  
~~Implementing standard and maintenance plugins~~  
Re-implementing IRC-Bot plugins

Checked with Codacy
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b042f31ae2c747f6a7309a6b3c57b761)](https://www.codacy.com/app/Chaos99/MatrixByteBot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Chaos99/MatrixByteBot&amp;utm_campaign=Badge_Grade)

## Build instructions
### build environment
#### base system
-   WinPython 3.6.6.2 including Python 3.6.6
-   Also tested with Python 3.5 on Debian Linux 9 (Stretch)
-   pip 18.1
-   virtualenv 16.0.0
-   tmux for start/stop/update scripts on Linux
  
#### Inside a python virtual environment
-   the matrix sdk package <https://github.com/matrix-org/matrix-python-sdk>
-   schedule package <https://pypi.org/project/schedule/>

#### Tipp
-   if dependency building fails for obscure reasons, delete
  Pipfile and re-add dependencies manually via pipenv 

### development hints
-   subclass Plugin in plugin.py for own plugins
-   (re-)implement at least 
-   \_\_init\_\_() for setting up the plugin
-   callback() for the code to be executed on keyword recognition
-   get_help() to return a short help text and usage description

#### Setup
-   call superclass constructor with ```Plugin.__init__(self, name, bot)```
-   register regex match rules like ```self.add_matcher(re.compile("![Dd]ates"))``` (you can add multiple)
-   register scheduled calls like ```bot.schedule.every(1).minutes.do(self.dates_announce_next_talks)```
-   save reference to bot for later use in scheduled tasks if needed (e.g. as ```self.bot```)

#### callback
-   send messages via ```room.send_text()```
-   get calling command via ```event['content']['body']``` for further analysis or matching

#### get_help()
-   return string for us ein !help command.
-   approx. one line per command/function
-   use "\n" in string for line breaks

#### scheduled tasks
-   any function or method can be scheduled via registration in \_\_init\_\_
-   there is no ```room``` or ```event``` parameter, so send messages to all rooms via ```self.bot.all_rooms.send_text()```


## Usage instructions
1. Change private_settings.py with username, password, servername and room
2. use 'git update-index --assume-unchanged private_settings.py' to no longer track changes and not accidentally upload your password
3. Start with ./start.sh (will start the bot inside a tmux shell by the name of 'bytebot')
4. add ./gitupdate.sh to your crontab if you want to track github changes to the current branch (bot will stop, update, restart if changes are available)
5. use 'tmux a -t bytebot' to connect to the session and see the terminal printout
6. use ./stop.sh to stop the process (but keep the tmux session)
7. use 'tmux kill-session -t bytebot' to also close the session

## License and Credits
See LICENSE file for GPLv3 license of this software.

Uses (but not includes) packages and libraries as listed above and below.
Links to original sources are given as documentation and credit to the authors.

Uses 
Scriptacular - gitupdate.sh
Copyright 2013 Christopher Simpkins
MIT License

schedule python package <https://pypi.org/project/schedule/>
Daniel Bader - @dbader_org - <mail@dbader.org>
MIT license

Based on (and contains snipets of code from) 
<https://github.com/Bytespeicher/Bytebot>
MIT License

See LICENCSE_MIT file for the license text.

The matrix bot api at 
<https://github.com/shawnanastasio/python-matrix-bot-api>
GPLv3 License
was part of this project but has since been completely removed.
