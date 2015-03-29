# Roastero
A coffee roasting application to control the Fresh Roast SR700.

## Dependencies
- Python3
- PyQt5
- Qt5
- Matplotlib 1.4.0+

## Usage


## Setup a Development Environment
### Mac
    git clone https://github.com/Roastero/Roastero.git
    cd Roastero
    brew install Python3
    pip install virtualenv
    virtualenv env -p Python3
    source env/bin/activate
    pip install matplotlib pyserial
    brew install PyQt5 qt5
    cp -r /usr/local/Cellar/pyqt5/5.4/lib/python3.4/site-packages/PyQt5 env/lib/python3.4/site-packages/
    cp /usr/local/lib/python3.4/site-packages/sip* env/lib/python3.4/site-packages/

#### Patching PySerial for Mac
While developing the application we found a bug in the PySerial library.
We tried to contact the developers but with no luck as of 2-1-15(v2.7).
For this reason you will have to manually patch Pyserial. It's not
that hard though. It's simply copying a file over.

    cp PySerial\ Patched\ Files/list_ports_osx.py env/lib/python3.4/site-packages/serial/tools/list_ports_osx.py

This should fix PySerial for now.

### Windows

## Fedora 21 Linux
    git clone https://github.com/Roastero/Roastero.git
    cd Roastero
    sudo pip3 install virtualenv
    virtualenv env -p python3
    source env/bin/activate
    sudo pip3 install pyserial matplotlib python3-pyqt5

### Ubuntu Linux
    git clone https://github.com/Roastero/Roastero.git
    cd Roastero
    sudo apt-get install python3 python3-pip qt5-default libfreetype6-dev
    sudo pip3 install virtualenv
    virtualenv env -p Python3
    source env/bin/activate
    sudo pip install pyserial python3-matplotlib python3-pyqt5


## License
The code is being released under GPL v3.
