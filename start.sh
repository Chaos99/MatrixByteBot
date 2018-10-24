#!/bin/bash
source env/bin/activate
tmux new-session -d -s bytebot 'pipenv run python3 main.py'