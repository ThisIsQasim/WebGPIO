# WebGPIO
A simple web UI for controlling the GPIO pins on a Raspberry Pi.

To setup make sure you have flask installed

    sudo apt install python3-pip libpython3-dev
    sudo pip3 install setuptools wheel
    sudo pip3 install flask pyyaml

Clone the repo and create a config file named config.yml in the repo folder. Define pin numbers, in BCM format, grouped into "Rooms" and "Appliances" in config.yml. See exampleconfig.yml for reference

    git clone https://github.com/ThisIsQasim/WebGPIO
    cd WebGPIO
    cp exampleconfig.yml config.yml

Run with python

    python3 backend.py     

Access the UI at http://pi_ip_address:8000
