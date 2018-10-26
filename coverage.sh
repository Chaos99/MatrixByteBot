#!/bin/bash


export CODACY_PROJECT_TOKEN=5fea6d75e993451692a05f3eaece186b
coverage run main.py
coverage xml
python-codacy-coverage -r coverage.xml

