Fresh Roast SR700 Communication Protocol
========================================

All of the communication between the SR700 and the computer are actually
happening over serial. The device contains a USB to Serial adapter that uses
the WCH CH341 chipset. With this it creates a virtual serial port that the
program and roaster communicate over. Each of them send 14 byte packets back
and forth between each other. All of the information below was found by sniffing
the communications between the roaster and the program on the serial port. This
was done in attempt to provide a reference point to create a better SR700
interface and to improve the capabilities of the SR700 when a computer is
attached. Looking at the protocol between two it is possible to have a computer
act at a temperature controller. Rather then just using the predetermined Low,
Medium, and High heat settings. With that below is the basic packet structure
of the serial communications between the devices.

|Packet Header|ID Field?|Flags|Control|Fan Speed|Timer|Heat Control|Current Temperature|Footer|
|-------------|---|-----|-------|---------|-----|------------|-------------------|------|
|2 bytes|2 bytes|1 byte|2 bytes|1 byte|1 byte|1 byte|2 bytes|2 bytes|

An example Packet would be like below

|Packet Header|ID Field?|Flags|Control|Fan Speed|Timer|Heat Control|Current Temperature|Footer|
|-------------|---|-----|-------|---------|-----|------------|-------------------|------|
|AA AA | 61 74 | 63 | 02 01 | 01 | 32 | 01 | 00 00 | AA FA |

Packet fields
=============
Below I'll describe each field and how they are used.

Packet Header (2 bytes)
-----------------------
This field is 2 bytes and almost always `AA AA`. The one exception to this is
that when you're initializing the communications the with the roaster the
computer sends `AA 55`.

ID Field? (2 bytes)
-------------------
The next 2 bytes I do not know what they do. Every single communication they
were always `61 74`. I'm assuming it's some kind of ID field but could be
completely wrong.

Flags (1 byte)
--------------
This field of the packet can be used to differentiate between whether the
roaster or the computer sent the packet and a few other things. below are the
possible values that can be in the field and what they mean.

`63` - This value means the packet was sent from the computer

`00` - The packet was sent by the roaster

The above will give you some insight on whose sending the packet. Although there
are other values that could be in these field that won't give you that insight.
The following values are used in this field when a recipe sequence is being
communicated between the roaster and the computer.

`AA` - Programming sequence line with more in the sequence to follow

`AF` - Last line in a Program's sequence

`A0` - Sent by the roaster to tell the current manual mode settings on the
roaster

Control (2 bytes)
-----------------
This section is the part of the packet that control the start and stop of the
roaster. There are many options that can be passed with this field. Below is the
list of them along with what they trigger.

`02 01` - Pre-roast idle (Shows current timer and fan speed values)

`04 02` - Roast

`04 04` - Cooling Process

`08 01` - Stops roast / Makes roaster sleep (Displays "-" in both fan speed and
timer fields on the roaster)

Fan Speed (1 byte)
------------------
This field is actually quite self explanatory. It just the fan speed in hex.
Below are the possible values you can pass it.

`01`,`02`,`03`,`04`,`05`,`06`,`07`,`08`, or `09`

Timer (1 byte)
--------------
This field is also very simple. It's just the current timer reading in hex. for
example 1 and a half minutes would be translate to 1.5 or 15. This is then
translated into hex as `0F`. Another example be that 5.9 minutes (5 minutes and
54 seconds) would be `3B` in hex.

Heat Control (1 byte)
---------------------
This field is just the heat setting for the roaster at that time. The values are
also easily interpreted as the following.

`00` - No Heat (Cooling)

`01` - Low Heat

`02` - Medium Heat

`03` - High Heat

Temperature (2 bytes)
---------------------
This field is just the temperature inside the roaster encoded in hex. When the
roaster doesn't read a temperature of 150°F or higher it sends the following hex
`FF 00`. When is does read a temperature it's simply that temperature encoded in
hex. For example 352°F is `01 60`.

Footer (2 bytes)
----------------
This field to always seems be the following `AA FA`. It simply the field that
signifies the end of the transmission.

Packet Sequences
================
Being able dissect a packet is enough interpret the communications but if you're
wanting to communicate yourself you will need to know in which order to send the
packets and when to send packets. In this section I'll describe exactly that.

To start off every communication between the roaster and the computer is
initiated by the computer. It is initiated with a packet that looks like the
below packet.

`AA 55 61 74 63 00 00 00 00 00 00 00 AA FA`

This packet is simply a blank packet with a `55` in the second byte of the
packet. This then signals the roaster to send back it's current configuration
on the roaster. This configuration will consist of the USB downloaded recipe and
the current manual setting on the roaster. Below is an example of the data that
roaster would send back.

`AA AA 61 74 A0 00 00 09 3B 02 00 00 AA FA` <-- Manual setting currently on the
roaster

`AA AA 61 74 AA 00 00 09 03 03 00 00 AA FA` <-- First line of the USB program
currently on the device

`AA AA 61 74 AA 00 00 09 01 02 00 00 AA FA` <-- Second line of the USB program
currently on the device

`AA AA 61 74 AF 00 00 09 1C 00 00 00 AA FA` <-- Last line of the USB program
currently on the device which in this case is the cooling cycle

It sends the above packets all one right after another. It doesn't wait for the
computer to respond, until after the last line of sequence is sent. The last
packet that's sent is donoted by the `AF` as the fifth byte in the packet.

After this computer sends back the heat, fan speed, and time settings it wants
the roaster to be set to. This is all sent in a single packet like the
following.

`AA AA 61 74 63 02 01 01 3B 01 00 00 AA FA` <-- heat=low, fan speed=1, time=5.9
minutes

The roaster then sends back the current settings. Basically confirming the
change of settings and the current temperature of the roaster if it's 150°F or
higher. The response paket for the above packet would most like be the
following.

`AA AA 61 74 00 02 01 01 32 01 FF 00 AA FA`

You should be able to interpret the above packet with the above section.
Although it's pretty much the same as the sent packet above except the `63` in
the 5th byte is switched to `00`. The other change is the 2 byte temperature
field is now `FF 00` which means the current temperature is below 150°F.

This sequence of the computer sending a packet with the current settings and the
roaster confirming those setting with the addition of the temperature is
continually sent. Nothing will happen on the roaster until the 6th and 7th bytes
in the packet change. From the examples above the 6th and 7th byte are `02 01`
which means that roaster is just in an idle mode.

To actually start roasting you will continue with the above sequence of packets
except the 6th and 7th byte will change to `04 02`. This means that's entering
into a roasting mode. You continue changing the fan speed, heat, and the timer
fields according to your roast settings.

When you're ready to start cooling just switch the 6th and 7th byte to `04 04`.

When it's done just finish by changing the 6th and 7th byte to `08 01`.

Drivers
=======

Windows & Linux
---------------
The drivers should work out of the box. If you have problems you can always
the source from the official site here:
http://www.wch.cn/downloads.php?name=pro&proid=5

Mac OSX
-------
Download latest driver from the official site here:
http://www.wch.cn/downloads.php?name=pro&proid=5

Install these drivers. If you're running OSX Yosemite you will have to issue the
following command.

`sudo nvram boot-args="kext-dev-mode=1"`

Then reboot.
