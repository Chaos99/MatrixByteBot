#!/bin/bash
source env/bin/activate
#tmux new-session -d -s bytebot 'pipenv run python3 main.py'
#tmux send -t bytebot 'cd ${0%\*}' ENTER
tmux send -t bytebot 'pipenv run python3 main.py ' ENTER

