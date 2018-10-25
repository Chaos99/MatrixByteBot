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

## Build instructions
### build environment
- original setup includes
  - WinPython 3.6.6.2 including Python 3.6.6
  - Also tested with Python 3.5 on Debian Linux 9 (Stretch)
  - pip 18.1
  - virtualenv 16.0.0
  - tmux for start/stop/update scripts on Linux
  
  - Inside a python virtual environment:
    - the matrix sdk package https://github.com/matrix-org/matrix-python-sdk 
    - schedule package https://pypi.org/project/schedule/

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

schedule python package https://pypi.org/project/schedule/
Daniel Bader - @dbader_org - mail@dbader.org
MIT license

Based on (and contains snipets of code from) 
https://github.com/Bytespeicher/Bytebot
MIT License

See LICENCSE_MIT file for the license text.

The matrix bot api at 
https://github.com/shawnanastasio/python-matrix-bot-api
GPLv3 License
was part of this project but has since been completely removed.
