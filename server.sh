#!/bin/bash

if python3 --version 2>/dev/null
then
    python3 app.py "$@"
else
    echo "Cannot find python"
    exit 1
fi