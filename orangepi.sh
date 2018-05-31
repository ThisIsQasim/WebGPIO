#!/bin/bash
git checkout backend.py
git pull
sed -i 's/RPi/OPi/g' backend.py
python3 backend.py