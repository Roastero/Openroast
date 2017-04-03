This information is aimed at developers who are maintaining the Openroast application.  Familiarity with python, several desktop operating systems, as well as scripting in several languages is assumed.

This document describes the steps that a developer must execute to successfully create a distributable Openroast application package for Windows and Mac OS operating systems.

## General Good-to-knows

- As of Openroast 1.2, python 3.5 is the required version of python to build and run Openroast.  This is because PyQt5, which is a python GUI application toolkit (specifically, a python wrapping over the Qt5 multi-platform GUI toolkit), is significantly easier to deal with in Python 3.5+.

---
# Building the Openroast 1.2 app - Windows 10 - 64 & 32 bit

(The following instructions were developed for a fresh Windows 10 Pro install running in a Virtualbox VM with Ubuntu 14.04 as the host OS.)

It is assumed that the operations herein are being performed on a fresh install of Windows 10.  A fresh install will not have any of the dependencies required to build Openroast.  These instructions, and the associated tools that are downloaded during the process, will guide the developer from a Win10 fresh install state, to a Win10 version of Openroast ready to distribute.

The script creates a 64-bit or 32-bit build based on the operating system it is running on. To build a 64-bit version of the app, use a Win10 64-bit OS machine and follow the instructions below. To build a 32-bit version of the app, use a Win10 32-bit OS machine and follow the instructions below.

## 1. Starting from nothing - Setting up the development environment

If you do not have git set up, you can get all necessary build tools set up by downloading a single file from the Openroast github project, namely, the [build_win.ps1](https://github.com/Roastero/Openroast/blob/master/build_win.ps1) file.

Alternately, if you already have git installed, you should clone the Openroast project into the folder of your choice, and go directly to step 3 in the instructions below.

1. Download build_win.ps1.
2. Place it in a folder in which you intend to create all the necessary project folders for this project.  (In a later step, the script will eventually fetch the files and place them under the folder \[YourCurrentPath\]\Roastero\Openroast.)
3. Start a PowerShell command prompt. You need to launch PowerShell with the "Run as Administrator" option. One way to do this is to type PowerShell in the search bar, then right-click on the PowerShell app icon that appears, and select "Run as Administrator".
4. We must set up elevated privileges to run the scripts in this PowerShell window.  The easiest way to achieve this is to enter the command `Set-ExecutionPolicy RemoteSigned`. This allows local scripts to run unsigned.
5. In the PowerShell window, cd to where you've placed the build_win.ps1 script. (If you've cloned the Openroast project already, the file is in the project root folder.)
6. Type `build_win.ps1 -tool_install` and press Enter.  The following things will happen:
    1. installer downloads for python 3.5 for Windows, git, and NSIS. (Note that the git installer insists on re-installing git every time.  If this is something you want to avoid, you should modify build_win.ps1 to not download nor install git.)
    2. Install python 3.5 for Windows, git, and NSIS
7. You are now in a position to fetch the source code from github, if you haven't done so already.

## 2. Getting the source code

If you have already cloned the branch of interest (almost always master...) from http://github.com/Roastero/Openroast, you can skip this section.

Assuming you have a PowerShell window opened to the directory of interest as directed in the previous steps, you're ready to fetch the code from github.

1. At the Power Shell prompt, type `build_win.ps1 -git_fetch` and press Enter.  You are now fetching the head of the master branch. (To fetch a different branch, type `build_win.ps1 -branch_name <name> -git_fetch` instead, where <name> is the name of the branch you want to fetch.)
2. You now have the code locally.  You'll want to `cd Roastero/Openroast` and continue working from there.

## 3. Getting project dependencies

1. Type `build_win.ps1 -python_build_tool_install` and press Enter.  The following things will happen:
    1. Install a couple of python-based tools. Note that if this fails (probably because you've just installed python 3.5), you may need to close the PowerShell window and open a new one, and re-invoke the script with `build_win.ps1 -python_build_tool_install`.

## 4. Incrementing the version number

*This part of the script does not currently work, as bumpversion does not execute properly from PowerShell in Windows.  Tagging and versioning is operated from Linux at the moment, and the Windows build cannot successfully change the version string and tag the source. There is no plan to fix bumpversion execution in the Windows script.*

In some instances, you may want to increment some part of the version number.  The bumpversion utility is used to perform version number incrementing.  Since a release will typically involve multiple platforms (Windows, Mac OS, Linux source install...), it is recommended that the maintainer learn to use the bumpversion utility outside of the build script process, before starting to create installer builds.

## 5. Creating a Windows Installer

Assuming you're in PowerShell and currently in the `[YourWhateverFolderPath]\Roastero\Openroast` directory, you can create an installer build by typing `build_win.ps1 -make_installer` and pressing Enter.  The ZIP containing the installation package will be created in the folder `[YourWhateverFolderPath]\Roastero\Openroast\build`.   You'll want to test this installer on a separate Windows machine to verify functionality.

## 6. Posting the installer on Github

At this point, you have a ZIP package that you believe is functional and ready for distribution.

Github currently makes it easy to create a release and attach installer files to the release.  With proper use of bumpversion, tags are created in the source repository and are visible in the releases tab on the Openroast github site. Release notes and files can be attached to a particular commit tag.  See existing release notes and attachments for guidance on creating a new release.

Typically, the ZIP is attached to the release and users can download the installer from there.

---
# Building the Openroast app - Mac OS X 10.10.5

(The build script and following instructions were developed on a Macbook Pro 2.4 GHz Intel Core 2 Duo (circa 2011) running OS X 10.10.5 Yosemite.)

It is assumed that the operations herein are being performed on a Macbook that has no developer tools installed. These instructions, and the associated tools that are downloaded during the process, will guide the developer through the process of generating a distributable Mac app.

## 1. Starting from nothing - Setting up the development environment

If you do not have homebrew or git set up, you can get all necessary build tools set up by downloading a single file from the Openroast github project, namely, the build_mac.sh file.

Alternately, if you already have homebrew and git installed, you should clone the Openroast project into the folder of your choice, and go directly to step 3 in the instructions below.

Note that you need to be an admin user on your Mac in order to successfully build Openroast.

1. Download build_mac.sh.
2. Place it in a folder in which you intend to create all the necessary project folders for this project.  (In a later step, the script will eventually fetch the files and place them in the folder `[YourCurrentPath]/Roastero/Openroast`.)
3. Start Terminal. (Don't know where that app is? You'll find it under Applications/Utilities.)
4. In the Terminal window, cd to where you've placed the build_mac.sh script. (If you've cloned the Openroast project already, the file is in the project root folder.)
6. Type `./build_mac.sh` and press Enter.  The following things will happen:
a. Download & install/update homebrew, pyenv, and python 3.5.3.
b. A warning will appear with regards to pyenv.  Please read the warning and follow the instructions provided by the warning. pyenv needs certain environment variables set up at Terminal launch time, and the warning tells you how to do this.
7. Enter `./build_mac.sh -n -p`. This will install Openroast app python package requirements and python build tools required to make the installer.
8. You are now in a position to fetch the source code from github (if you haven't done so already).

## 2. Getting the source code

If you have already cloned the branch of interest (almost always master...) from http://github.com/Roastero/Openroast, you can skip this section.

Assuming you have a Terminal window opened to the directory of interest as directed in the previous steps, you're ready to fetch the code from github.

1. At the Terminal prompt, type `./build_mac.sh -n -f` and press Enter.  You are now fetching the head of the master branch. (To fetch a different branch, type `./build_mac.sh -n -b <name> -f` instead, where <name> is the name of the branch you want to fetch.)
2. You now have the code locally.  You'll want to `cd Roastero/Openroast` and continue working from there.

## 3. Incrementing the version number

This is not a mandatory step.

In some instances, you may want to increment some part of the version number.  The bumpversion utility is used to perform version number incrementing.  Since a release will typically involve multiple platforms (Windows, Mac OS, Linux source install...), it is recommended that the maintainer learn to use the bumpversion utility before starting to create installer builds, outside of the build script process.

If you want to increment any part of the version number, you can do so by
1. making sure you're in the Openroast root folder in Terminal;
2. typing `./build_mac.sh -n -i <part>`, where <part> is one of major, minor, patch, release, or iter. (Type `build_mac -h` to read the help text for this script to know more.)
3. This will only work if your repository is clean (meaning, all changes have been committed). If that isn't the case, bumpversion will refuse to increment the version number.
4. Once you have executed this successfully, you should `git push --tags origin <branch-name>` to commit the version tag and associated file changes to the Openroast project origin.  (If this is unclear to you, you should contact a project maintainer for guidance...)

## 4. Creating a Mac app contained in a DMG

Assuming you're in Terminal and currently in the `[YourWhateverFolderPath]\Roastero\Openroast` folder, you can create an app build by typing `./build_mac.sh -n -m` and pressing Enter.  A disk image (DMG) containing the app will be created in the folder `[YourWhateverFolderPath]/Roastero/Openroast/dmg`.   You'll want to test this app on a separate Mac machine to verify functionality.

## 5. Posting the installer on Github

At this point, you have an app packaged as a DMG that you believe is functional and ready for distribution.

Github currently makes it easy to create a release and attach installer files to the release.  With proper use of bumpversion, tags are created in the source repository and are visible in the releases tab on the Openroast github site. Release notes and files can be attached to a particular commit tag.  See existing release notes and attachments for guidance on creating a new release.

Typically, the DMG is attached to the release and users can download the DMG from there.
