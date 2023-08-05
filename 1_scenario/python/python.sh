#!/bin/sh

# exit on error
set -e
# turn on command echoing
set -v

python test2.py
python test3.py
python saveDcDpconc.py
python Fig2.py
python Fig2CT.py
python print_CT.py

