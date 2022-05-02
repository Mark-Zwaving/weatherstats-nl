# WeatherstatsNL

Commandline python3 program to calculate weather statistics with data from the knmi.  

## Download/clone weatherstats-nl
*Download from:*  
https://github.com/Mark-Zwaving/weatherstats-nl  

*With git clone*
```
git clone https://github.com/Mark-Zwaving/weatherstats-nl
```

## Python3
Program makes use of of python3 *version >= 3.7.3*  
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
```
sudo apt-get install libffi-dev  
```  
*Recompile and instal python3.7 again*  
  
### Install necessary python3 libraries  
For WeatherStatsNL and the builtin library common, some python3 libraries needs to be installed    
  
Which libraries?  
See file requirements.txt  

**Install all libraries for weatherstats-nl**  
```
python3 -m pip install -r requirements.txt  
```

**Install all libraries in a virtual environment (recommended)** 
  
*Install a virtual environment*  
```
python3 -m pip install virtualenv
``` 
*Create a virtual envronment with python3.7*  
```
virtualenv venv-py37 --python=/path/to/python3.7
```  
*Activate a virtual environment* 
```
source venv-py37/bin/activate
```  
*Install libraries*  
```
python3 -m pip install -r requirements.txt
```  

### Start program weatherstats-nl
```
python3 wstats-nl.py
```  
