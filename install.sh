#!/bin/bash  

# Remove apache web server
sudo update-rc.d -f apache remove

sudo apt-get install cherokee


sudo apt-get install python-pip
sudo apt-get install git
sudo apt-get install python-flup
git clone https://github.com/timothyclemans/checklistsforglass.git
sudo pip install -r checklistsforglass/requirements.txt
