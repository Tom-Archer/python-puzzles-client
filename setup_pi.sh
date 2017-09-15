#!/bin/bash
echo "Setting up Masterclass Raspberry Pi."

echo "Downloading Python Puzzles Client Software"
mkdir /home/pi/Python
cd /home/pi/Python
git clone https://github.com/Tom-Archer/python-puzzles-client.git
cd /home/pi/Python/python-puzzles-client/library
sudo python3 setup.py install
sudo rm -rf /home/pi/Python/python-puzzles-client/

echo "Enabling Power-saving."
echo "wireless-power off" | sudo tee -a /etc/network/interfaces > /dev/null
echo "options 8192cu rtw_power_mgnt=0 rtw_enusbss=0" | sudo tee -a /etc/modprobe.d/8192cu.conf > /dev/null

echo "Installing matplotlib."
sudo apt-get -y install python-matplotlib

echo "Uninstalling bloat."
# https://andrewvaughan.io/raspbian-i-love-you-but-youre-fat/
sudo apt-get -y  purge bluej greenfoot oracle-java8-jdk dillo epiphany-browser galculator netsurf-gtk libreoffice libreoffice-avmedia-backend-gstreamer libreoffice-base libreoffice-calc libreoffice-draw libreoffice-gtk libreoffice-impress libreoffice-java-common libreoffice-math libreoffice-report-builder-bin libreoffice-sdbc-hsqldb libreoffice-writer minecraft-pi nodered nuscratch python-minecraftpi python3-uno scratch scratch2 sense-hat smartsim sonic-pi timidity wolfram-engine python-sense-emu python3-sense-emu python-sense-emu-doc sense-emu-tools

echo "Removing Python games."
sudo rm /usr/share/raspi-ui-overrides/applications/python-games.desktop 
sudo rm -R /home/pi/python_games

echo "Installing Docker."
curl -sSL https://get.docker.com | sh
sudo systemctl enable docker

echo "Cleaning up!"
sudo apt-get -y autoremove
sudo apt-get clean