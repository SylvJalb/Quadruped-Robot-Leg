# Setup
For this project i use python 3.10

## Odrive Installation
On terminal :       
``` bash
sudo pip3 install --upgrade odrive
```

## Setup python environment
Run a virtual environment and install the requirements      
``` bash
pip3 install -r requirements.txt
```

## Setup env
Create a new file named `env.py` and put your informations :        
``` python
ODRIVE_1_SN = "XXXXXXXXXXXX" # converted in Hexadecimal
ODRIVE_2_SN = "XXXXXXXXXXXX" # converted in Hexadecimal
MODE = "motor" # "simulation" or "motor"
```