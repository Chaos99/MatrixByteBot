# MatrixByteBot
## Description
 A bot living in the channels of the Erfurt Hackspace 'Bytespeicher' or the Makerspace,
 serving its users.

 Interfacing a matrix network, using the matrix-sdk.
 Written in Python 3.6.

## Status
~~Concept phase and build environment setup~~
~~Prototyping login and triggering~~
Implementing standard and maintenance plugins

## Build instructions
### build environment
- original setup includes
  - WinPython 3.6.6.2 including Python 3.6.6
  - Also tested with Python 3.5
  - pip 18.1
  - virtualenv 16.0.0
  
  - Inside a python virtual environment:
    - the matrix sdk package https://github.com/matrix-org/matrix-python-sdk 

## Usage instructions
1. Create private_settings.py with a single line ```PASSWORD = "yourpassword"```
2. update USERNAME, SERVER and ROOM in main.py near the top
3. Start with ```pipenv run python3 main.py```

## Licenses
See LICENSE file for GPLv3 license of this software.

Uses (but does not include) packages and source code listed above.
Links to original sources are given as documentation and credit to the authors.

The matrix bot api at https://github.com/shawnanastasio/python-matrix-bot-api
was part of this project but has since been removed.
