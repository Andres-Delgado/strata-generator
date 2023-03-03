#!/bin/sh
export FLASK_APP=./strata-generator/index.py
pipenv run flask --debug run