#!/bin/bash
echo "Setting up Masterclass Raspberry Pi."

echo "Downloading Python Puzzles Client Software (for Python 2.7)"
mkdir /home/pi/Python
cd /home/pi/Python
git clone https://github.com/Tom-Archer/python-puzzles-client.git
cd /home/pi/Python/python-puzzles-client/library
sudo python2.7 setup.py install
sudo rm -rf /home/pi/Python/python-puzzles-client/

echo "Done!"
