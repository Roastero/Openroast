You do not need to install any software other than what is in the contents of the installation package.  All necessary software is provided in the package.

## Software and Driver Installation

1. Download the latest Openroast Windows installation package from https://github.com/Roastero/Openroast/releases.  A 64-bit and a 32-bit version are available.
2. Double-click on the ZIP file.
3. In the ZIP file, you will find 3 files:
    1. a README file that is essentially the same as what you are reading here;
    2. *CH341SER.EXE.zip*, which is the installer for the Windows USB drivers required to communicate withthe Freshroast SR700;
    3. *Openroast_v1.2.x_Win10_xxbit.EXE*, which is the Windows 10 installer for either 64-bit or 32-bit Windows, depending on which Windows package you downloaded.
4. Next, you may have to install the driver.
    1. If you previously installed the Freshroast SR700 app that comes with the roaster, the drivers have already been installed and therefore, you do not need to install the drivers. Go to step 5.
    2. If you have not installed the Freshroast SR700 app, then go ahead and double click on *CH341SER.EXE.zip*.  This will open the zip file.  Now, double-click on *CH341SER.EXE*, and install the USB driver.
5. Finally, install the Openroast app.  Double-click on *Openroast_v1.2.x_Win10_xxbit.EXE*, which will install the Openroast app.

## Launching the Openroast app

1. The installer does not put an Openroast shortcut on your desktop.  You will find the app icon in the Windows Menu (bottom left-hand corner button) under 'Recently Added' as well as listed in the applications starting with the letter 'O'.

![Image of Windows Menu Showing Openroast icon in Recently Added](https://github.com/Roastero/Openroast/blob/master/docs/wiki/img/Openroast_Windows_Install_Shortcut_Recent.png "Optional title")

![Image of Windows Menu Showing Openroast icon in Apps](https://github.com/Roastero/Openroast/blob/master/docs/wiki/img/Openroast_Windows_Install_Shortcut_O.png "Optional title")

## Notes and Observations

1. Some people have reported that Openroast sometimes does not detect a connected roaster. Although the root cause has not been found, all evidence points to an incompatibility between the roaster hardware and a certain class of USB 3 ports.  For example, on a Dell XPS 9343 laptop, the roaster is recognized only when connected to the left USB port, and not the right USB port.  Some people have successfully worked around this issue by connecting a USB 2 hub to their USB 3 port, and plugging the roaster into the USB 2 hub.  A sure sign that the USB port is at issue is when the software supplied with the Freshroast SR700 itself cannot recognize the roaster.
