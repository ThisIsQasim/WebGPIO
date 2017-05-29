#!/bin/bash
CLOUDHOST=aws.thisisqasim.com
LANADDRESS=$(ifconfig  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}')
WANADDRESS=$(curl http://icanhazip.com)

curl http://{$CLOUDHOST}/ip/{$LANADDRESS}/

while true; do 

ip monitor address | while read  -t 60 output
do
 if echo $output | grep -v Deleted | grep eth0 | awk '{ print $4}' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}"; then
 NEWADDRESS=$(echo $output | grep -v Deleted | grep eth0 | awk '{ print $4}' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}")
 LANADDRESS=$NEWADDRESS
 curl http://{$CLOUDHOST}/ip/{$LANADDRESS}/
 exit 0
 fi
done

PUBLICIP=$(curl http://icanhazip.com)

if echo $PUBLICIP | grep $WANADDRESS; then
curl http://{$CLOUDHOST}/ip/{$LANADDRESS}/
fi

done