# WeatherstatsNL

Commandline python3 program to calculate weather statistics with data from the knmi  

## Python3
Programm makes use of of python3 version >= 3.7.3  
Install it from: https://www.python.org/ftp/python/  

### Install for windows
Pick a correct version: https://www.python.org/downloads/windows/  

### Install from source (linux)
```
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar xzvf Python-3.7.9.tgz
cd Python-3.7.9  
./configure --prefix="/usr/local" --with-openssl="/usr" --enable-shared --enable-optimizations  
make  
make altinstall  
```
Ctypes error :(  
ModuleNotFoundError: No module named '\_ctypes'  
For linux debian install:  
>>> sudo apt-get install libffi-dev  
Recompile and instal python3.7 again  
  
### Install necessary python3 libraries  
For WeatherStatsNL and the builtin library common, some python3 libraries needs to be installed    
  
Which libraries?  
See file requirements.txt  
  
Install tutorial: 
```
# Install all libraries for weatherstats-nl  
python3 -m pip install -r requirements.txt  
  
# Install with a virtual environment (recommended):  
  
# Install virtual environment  
python3 -m pip install virtualenv  
# Create virtual envronment with python3.7  
virtualenv --python=/path/to/python3.7  
# Activate venv  
source venv/bin/activate  
# Install libraries  
python3 -m pip install -r requirements.txt  
```

### Start weatherstats-nl
```
python3 wstats-nl.py  
```
