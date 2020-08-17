# Sinkler Automatic Weighing System
Python program to automatically control a hopper/augar system for mixing ingredents to be milled for chicken feed.

## Software Installation Instructions
### Ensuring USB works correctly
* Ensure your USB is called "RATIONUSB" and copy rations.xlsx to it
* Plug in your USB and run ```sudo blkid``` noting the UUID of your device (it will look something like ```5C24-1453```)
* Run ```sudo nano fstab``` to edit the fstab file
* Add to the bottom: ```UUID=*INSERT YOUR UUID HERE*  /media/pi/RATIONUSB  vfat  defaults,nofail  0  0```


### Main Setup
* Install latest version of Raspberry Pi OS onto Raspberry Pi (tested with Buster)
* Ensure you have Python 3.7 or later installed
* Install the openpyxl module with ```sudo pip3 install openpyxl```
* Clone this Github repository
* Run ```sudo python3 SAWS/SAWS.py```

### To run at startup
* Ensure ```~/.config/lxsession/LXDE-pi/autostart``` exists
* Edit it with ```nano ~/.config/lxsession/LXDE-pi/autostart``` 
* Ensure the file looks like this:
```
#@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
#@point-rpi
@cd /FULL_INSTALL_PATH/SAWS && ./SAWS.sh
```
* Reboot
