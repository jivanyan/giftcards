#!/bin/bash

sudo apt-get update
sudo apt-get install -y git make

sudo apt-get install -y python-pip
sudo apt-get install -y python-dev

sudo HOME=/tmp/ pip install --upgrade virtualenv==1.11.6

sudo pip install -r requirements.txt
pushd /tmp/
