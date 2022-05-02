# WeatherstatsNL

Commandline python program to calculate weather statistics with data from the knmi

## Install python libraries
python3 wsnl.py
For WeatherStatsNL and the dependency library common there need to be some libraries installed    
See requirements.txt
Install command:
python3 -m pip install -r requirements.txt

## Example install python3

Install > python3.7
Download correct version:
https://www.python.org/ftp/python/3.7.13/Python-3.7.13.tgz

tar xzvf https://www.python.org/ftp/python/3.7.13/Python-3.7.13.tgz

cd Python-3.7.13  
./configure --prefix="/usr/local" --with-openssl="/usr" --enable-shared --enable-optimizations  
make  
make altinstall  

### Ctypes error :(
ModuleNotFoundError: No module named '\_ctypes'  
Linux debian install: 
sudo apt-get install libffi-dev  
  
Recompile and instal python3.7 again  