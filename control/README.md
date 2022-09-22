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
# ODRIVE 1 is connected to the arm and forearm
ODRIVE_1_SN = "XXXXXXXXXXXX" # converted in Hexadecimal

# ODRIVE 2 is connected to the shoulder
ODRIVE_2_SN = "XXXXXXXXXXXX" # converted in Hexadecimal

# The MODE to run the program
MODE = "motor" # "simulation" or "motor"
```

## Run the test program 
This test program run the following instructions :      
- Detect ODRIVE Cards
- Setup with parameters
- Run the calibration (This may take some time...)
- Run the walking loop

On your raspberry pi, run the test program :
``` bash
cd ./tests
python3.10 ./test_leg_class.py
```

If the calibration fail, disconnect and reconnect the cards from current, retry to run the program.