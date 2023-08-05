#!/bin/sh

# exit on error
set -e
# turn on command echoing
set -v

python test2.py
python test3.py
python discussion_a.py

python discussion_b.py
