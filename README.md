# WeatherstatsNL
---
Commandline python3 program to calculate weather statistics with data from the knmi.  
---

### Download weatherstats-nl
 - From the web:  
<a href="https://github.com/Mark-Zwaving/weatherstats-nl" target="_blank">https://github.com/Mark-Zwaving/weatherstats-nl</a>  

 - Download with git:   
```git clone https://github.com/Mark-Zwaving/weatherstats-nl```

### Python3
> Program makes use of of python3 *version >= 3.8*  
Install it from: *https://www.python.org/ftp/python/*  
For example version 3.8.18:  *https://www.python.org/ftp/python/3.8.18/*  
Use of Python3.8 is most save

### Install Python3 for windows
Pick a correct version:  
*https://www.python.org/downloads/windows/*  

### Install Python3 from source (Linux, Debian)
Source tutorial: *https://www.linuxcapable.com/how-to-install-python-3-9-on-debian-linux/* 
#### Make a download directory for python 3.8
```mkdir python3.8```
#### Goto directory python3.8
```cd python3.8```
#### Download python3.8
```wget https://www.python.org/ftp/python/3.8.18/Python-3.8.18.tar.xz``` 
#### Unzip python package 3.8
```tar -xvf Python-3.8.18.tar.xz``` 
#### Move map python3.8.18 to the shared library map python3.8
```sudo mv Python-3.8.18 /usr/local/share/python3.8```
#### Goto the shared python3.8 map
```cd /usr/local/share/python3.8/```
#### Install (possible) missing libraries for python3.8
```sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev libjpeg-dev zlib1g-dev -y ```
#### Configure source code 
``` ./configure --enable-optimizations --with-lto --enable-shared ``` 
#### Compile the source code
```make```
#### Make an alternative install for python3.8
```sudo make altinstall```
#### Add the shared python3.8 map to the shared dynamic linker
```sudo ldconfig /usr/local/share/python3.8```
#### Check the new python3.8 installation
```python3.8 --version```
  
#### Install necessary python3 libraries for weatherstats-nl 
#### Which python3 libraries are needed?  
*See file requirements.txt*  

#### Option 1: global installation
```python3.8 -m pip install -r requirements.txt```

#### Option 2: virtual envrionment installation
#### Install all libraries in an virtual environment (recommended)
#### Install venv for Python3.8
```python3.8 -m pip install venv``` 

#### In the map weatherstats-nl create an virtual environment named 'venv-py38' with the use of python3.8   
```python3.8 -m venv venv-py3.8```  

#### Activate the virtual environment 
```source venv-py3.8/bin/activate```  

#### Install all the needed python3 libraries from the file requirements.txt 
```python -m pip install -r requirements.txt ```  

## Start program weatherstats-nl
```python3 ws.py```  

### License
*GNU General Public License version 2 - GPLv2*
