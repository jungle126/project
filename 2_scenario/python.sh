#!/bin/sh

# exit on error
set -e
# turn on command echoing
set -v

python test1.py
python test7.py
python test_new.py

