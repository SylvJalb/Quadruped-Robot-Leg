# Environements
- **Production** code, developed in **Rust** (in `src` directory)      
- **Development** and **simulation** code, developed in **Python**. (in `dev` directory)        
It use the production Leg class, built with [PyO3](https://github.com/PyO3/pyo3), to have a Python library thanks to [maturin](https://github.com/PyO3/maturin).     

# Rust Setup
Install Rust with [rustup](https://rustup.rs/).     

Build the project, here, like this:    
```bash
cargo build
```

# Python Setup
For this project I use python 3.10 in a virtual environement with `pyenv`.

## Setup python environment
First of all, create an run a virtual environment:    
```bash
pyenv virtualenv 3.10.0 robot
pyenv activate robot
```
Then, install the requirements:      
``` bash
pip install -r ./dev/requirements.txt
```
After that, you can create the python library with `maturin`:   
*(Rust code must be built before)*    
```bash
maturin develop
```
Now, you can run Python codes in the `dev` directory.
```bash
cd dev
python test.py
```

# Deploy on the robot (raspberry pi)
Build the rust code in your computer:
``` bash
cargo build
```

Make sure you can do ssh connection with the raspberry pi and get the IP address of the raspberry pi.   

Copy the binary file `./target/debug/leg_control` and the parameters file `params.json` to the raspberry pi with `scp`.     
