#!/bin/bash

if pipenv --py 2>/dev/null
then
    $(pipenv --py) app.py "$@"
else
    echo "Cannot find python"
    exit 1
fi