#!/bin/bash
CLOUDHOST=aws.thisisqasim.com
LANADDRESS=$(ip addr  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}")
WANADDRESS=$(curl http://icanhazip.com)

curl http://{$CLOUDHOST}/ip/{$LANADDRESS}/

while true; do 

timeout 120 ip monitor address | while read output
do
 if echo $output | grep -v Deleted | grep eth0 | awk '{ print $4}' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}"; then
 LANADDRESS=$(echo $output | grep -v Deleted | grep eth0 | awk '{ print $4}' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}")
 curl http://{$CLOUDHOST}/ip/{$LANADDRESS}/
 fi
done

PUBLICIP=$(curl http://icanhazip.com)

if [ "$PUBLICIP" != "$WANADDRESS" ]; then
curl http://{$CLOUDHOST}/ip/{$LANADDRESS}/
WANADDRESS=$PUBLICIP
fi

done
