# WebGPIO
A simple web UI for controlling the GPIO pins on a Raspberry Pi. Define pin numbers (BCM) in <code>outPin</code> array and pin names in <code>pinName</code> array in file backend.py. Make sure you have flask installed.

    sudo apt install python3-pip libpython3-dev
    sudo pip3 install setuptools wheel
    sudo pip3 install flask pyyaml

Run with python

    python3 backend.py     

Access the UI at http://pi_ip_address:8000
