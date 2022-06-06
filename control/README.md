# Setup
For this project i use python 3.10

## Odrive Installation

On terminal :
``` bash
sudo pip3 install --upgrade odrive

echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="0d[0-9][0-9]", MODE="0666"' | sudo tee /etc/udev/rules.d/91-odrive.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Python setup
``` bash
pip3 install -r requirements.txt
```