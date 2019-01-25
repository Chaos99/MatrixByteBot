#!/bin/bash
# start all tests and upload result to CODACY server
py.test --ignore=plugins/ --cov=MatrixByteBot --cov-branch --cov-report xml tests/
export CODACY_PROJECT_TOKEN=5fea6d75e993451692a05f3eaece186b
python-codacy-coverage -r coverage.xml