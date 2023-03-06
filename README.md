# WeatherstatsNL
---
Commandline python3 program to calculate weather statistics with data from the knmi.  

---

## Download weatherstats-nl
*Download from* 
<a href="https://github.com/Mark-Zwaving/weatherstats-nl" target="_blank">https://github.com/Mark-Zwaving/weatherstats-nl</a>  

*With git clone*  
```git clone https://github.com/Mark-Zwaving/weatherstats-nl```

## Python3
Program makes use of of python3 *version >= 3.7.3*  
Install it from: *https://www.python.org/ftp/python/*  
For example version 3.7.9:  *https://www.python.org/ftp/python/3.7.9/*  

### Install Python3 for windows
Pick a correct version:  
*https://www.python.org/downloads/windows/*  

### Install Python3 from source (linux)
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
*Recompile and install python3.7 again*  
  
### Install necessary python3 libraries  
For WeatherStatsNL and the library common some python3 libraries needs to be installed    
  
Which libraries?  
*See file requirements.txt*  

**Install all libraries for weatherstats-nl**  
```
python3 -m pip install -r requirements.txt  
```

**Install all libraries in an virtual environment (recommended)** 
  
*Install the python library for to make an virtual environment*  
```
python3 -m pip install virtualenv
``` 
*In the map: weatherstats-nl*  
*Create an virtual environment named 'venv-py37' with the use of python3.7*  
```
virtualenv venv-py37 --python=/path/to/python3.7
```  
*Activate the virtual environment* 
```
source venv-py37/bin/activate
```  
*Install all the needed python3 libraries from the file requirements.txt*  
```
python3 -m pip install -r requirements.txt
```  

### Start program weatherstats-nl
```
python3 wstats-nl.py
```  

