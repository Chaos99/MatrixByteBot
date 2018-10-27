#!/bin/bash

pytest --cov=helpplugin --cov-append --cov-report xml
export CODACY_PROJECT_TOKEN=5fea6d75e993451692a05f3eaece186b
python-codacy-coverage -r coverage.xml