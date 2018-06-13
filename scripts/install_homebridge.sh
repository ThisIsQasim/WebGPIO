#!/bin/bash
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install -y libavahi-compat-libdnssd-dev build-essential

sudo npm install -g --unsafe-perm homebridge
#WiringPi for OrangePi Zero
cd ~
git clone https://github.com/xpertsavenue/WiringOP-Zero.git
cd WiringOP-Zero
chmod +x ./build
sudo ./build
npm install -g homebridge-gpio-cmd

npm install -g forever
npm install -g forever-service

sudo npm install homebridge-gpio-wpi2