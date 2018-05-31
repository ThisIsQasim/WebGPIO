# WebGPIO
A simple web UI for controlling the GPIO pins on a Raspberry Pi. 
To setup make sure you have flask installed. Then clone the repo and define pin numbers, in BCM format, grouped into "Rooms" and "Accesories" in config.yml

    sudo apt install python3-pip libpython3-dev
    sudo pip3 install setuptools wheel
    sudo pip3 install flask pyyaml

Run with python

    python3 backend.py     

Access the UI at http://pi_ip_address:8000
