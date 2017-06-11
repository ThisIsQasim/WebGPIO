# WebGPIO
A simple web UI for controlling the GPIO pins on a Raspberry Pi. Define pin numbers (BCM) in <code>outPin</code> array and pin names in <code>pinName</code> array in file backend.py. Make sure you have flask installed.

    sudo apt-get install python-pip
    sudo pip install flask

Run with python

     python backend.py
     
Access the UI at http://piIPAddress:8000
