*Windows and Mac end-users will want to stick to the installer packages posted in [releases section](https://github.com/Roastero/Openroast/releases), rather than have to work through the information on this page.*

Running Openroast from source is possible in Linux as well as in Windows and OS X. Setup varies by platform.

It is assumed that the reader is familiar with python, git, and shell scripting. If these terms aren't familiar to you, we suggest that you learn the basics of python and git source code control before reading any further.

- [Windows](#running-from-source-in-windows-10)
- [Mac](#running-from-source-in-mac-os-x)
- [Ubuntu 14.04](#running-from-source-in-ubuntu-1404-linux)


---

## Running from source in Windows 10

For Windows 10, setting up to run Openroast from source involves running partway through the Windows build script. The build script installs all necessary tooling, including Python 3.5.  If you already have another version of Python installed, the build script will not discriminate between installed Python versions. It is up to the reader to determine how to ensure that Openroast is developed and executed in a Python 3.5 environment.  (The author runs a bare Win10 installation in a VirtualBox VM for this purpose.)

### Alternative A (preferred)

1. Start from a bare Win10 machine, and follow all the Windows build instructions posted in [For Developers: Building a Distributable Package](https://github.com/Roastero/Openroast/wiki/For-Developers:--Building-a-Distributable-Package). At the end of that process, you will have set yourself to build the app correctly.
2. If you have yet to install the Windows USB driver for the Freshroast SR700 hardware, you should do so now.  You'll find the driver installer in the project files, at `[your_folder]\Openroast\build_tools\CH341SER.EXE.zip`.
3. In a terminal window, `cd [your_folder]\Openroast`.
4. At this point, to run Openroast, all you should need to do is type `python openroast\openroastapp.py` and the app should run.

*Note that if you have more than one version of Python installed on your machine, you'll need to specify python 3.5 during requirements installs and when running `openroast/openroastapp.py`.*

### Alternative B (cryptic)

1. Using git, clone or fork this project to the folder of your choice.
2. If you have yet to install the Windows USB driver for the Freshroast SR700 hardware, you should do so now.  You'll find the driver installer in the project files, at `[your_folder]\Openroast\build_tools\CH341SER.EXE.zip`.
3. Start a PowerShell terminal, making sure you can execute unsigned local scripts. You'll want to launch PowerShell as administrator, as well.
4. `cd [your_folder]\Openroast`.
5. `.\build_win.ps1 -tool_install`. This will install Python 3.5, Git for Windows, and NSIS 3.0. If you do not want some of these installed, modify the script accordingly.
6. `.\build_win.ps1 -python_build_tool_install`. This installs both Openroast's python package dependencies, as well as the python-based build tool dependencies. (You can `pip install -r` these instead, there are two requirements.txt files in the root folder that specify the dependencies.)
7. At this point, to run Openroast, all you should need to do is type `python openroast\openroastapp.py` and the app should run.

*Note that if you have more than one version of Python installed on your machine, you'll need to specify python 3.5 during requirements installs and when running `openroast/openroastapp.py`.*

---

## Running from source in Mac OS X

For Mac OS X, setting up to run Openroast from source involves running partway through the Mac build script. The build script installs all necessary tooling, including Python 3.5. The build script also installs pyenv and sets the python version for the folder to 3.5, so to make your life easier, you really should take advantage of the build script to set up your system to run from source.

1. Follow all the Mac build instructions posted in [For Developers: Building a Distributable Package](https://github.com/Roastero/Openroast/wiki/For-Developers:--Building-a-Distributable-Package). At the end of that process, you will have set yourself to build the app correctly.
2. If you have yet to install the Mac USB driver for the Freshroast SR700 hardware, you should do so now.  You'll find the driver installer in the project files, at `[your_folder]/Openroast/build_tools/SH34x_Install_V1.4.pkg`.
3. In a Terminal window, `cd [your_folder]/Openroast`.
4. At this point, to run Openroast, all you should need to do is type `python openroast/openroastapp.py` and the app should run.

---

## Running from source in Ubuntu 14.04 Linux

*This is the maintainer's primary setup. There should be equivalent means of setting up Openroast in other Linux variants, but they are not documented at this time.*

For Ubuntu, you are about to
1. Install python 3.5 in the `/opt` folder as an alternate version of python, as Ubuntu 14.04 relies on the 2.7 and 3.4 versions that are installed with the OS and you do not want to mess with those installations.
2. Install some 'possibly relevent' packages using apt-get.  'Possibly relevent,' because the maintainer installed these items following older versions of instructions for Openroast 1.0...
3. Run Openroast 1.2 using your python 3.5 install.

### Installing python 3.5

*The instructions in this section are derived from the instructions at http://askubuntu.com/questions/680824/how-do-i-update-python-from-3-4-3-to-3-5 .*

```
wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3.tar.xz
tar xfvJ Python-3.5.3.tar.xz
cd Python-3.5.3
./configure --prefix=/opt/python3.5
make
sudo make install
```
Your python 3.5 interpreter will be located in `/opt/python3.5/bin/python3.5`.

To facilitate use you can symlink these files to a location on your $PATH like so:

```
sudo ln -s /opt/python3.5/bin/python3.5 /usr/local/bin/py3.5
```

After this, just typing py3.5 from the command line will use python 3.5, while at the same time, python 3.4 will remain untouched, and will not cause any "breakage" on your system.

### Installing packages

You have to have installed python 3.5 in the manner described above for these instructions to work.

Installing necessary tools:
```
sudo apt-get install git libfreetype6 libfreetype6-dev
cd [desired_root_folder]
git clone https://github.com/Roastero/Openroast.git
cd Openroast
```

At this point, what you do depends on whether you intend on developing and testing, or simply running the app from source.

#### Setting up to run the app from source, no intent to develop

To simply run the app from source install using `setup.py` which will install all app dependencies:
```
py3.5 -mpip install .
```
*Be aware that if you invoke `pip3` on your machine, you're installing to the system's default python3 version. It's important to invoke pip for your python 3.5 install using `py3.5 -mpip` instead.*

#### Setting up to run the app and make code changes

The major difference here is you'll want to install with the `-e` option:
```
py3.5 -mpip install -e .
```
This should install all app dependencies. If it doesn't, you can explicitly install the dependencies:
```
py3.5 -mpip -r build-app-requirements.txt
```
### Running Openroast

After all that, to run the app, you can either

`/opt/python3.5/bin/openroast`

or, from the project root folder,

`py3.5 openroast/openroastapp.py`.

