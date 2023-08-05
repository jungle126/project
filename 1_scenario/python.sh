#!/bin/sh

# exit on error
set -e
# turn on command echoing
set -v

python python/test2.py
python python/test2.py
python python/test_new.py

