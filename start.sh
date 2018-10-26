#!/bin/bash
source env/bin/activate
#first run
#tmux new-session -d -s bytebot 'source env/bin/activate; pipenv run python3 main.py'
#subsequent runs
tmux send-keys -t bytebot 'source env/bin/activate; pipenv run python3 main.py' ENTER