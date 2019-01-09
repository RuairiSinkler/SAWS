# Sinkler Automatic Weighing System
Python program to automatically control a hopper/augar system for mixing ingredents to be milled for chicken feed.

## Software Installation Instructions
* Ensure your USB is called "RATIONUSB" and copy rations.xlsx to it
* Install usbmount with ```sudo apt-get install usbmount```
* Install the openpyxl module with ```sudo pip3 install openpyxl```


* Install latest version of Raspbian onto Raspberry Pi
* Clone this Github repository
* Run ```sudo python3 SAWS/SAWS.py```

### To run at startup
* Ensure ```~/.config/lxsession/LXDE-pi/autostart``` exists
* Edit it with ```sudo nano ~/.config/lxsession/LXDE-pi/autostart``` 
* Ensure the file looks like this:
```
#@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
point-rpi
sudo python3 FULL_PATH_TO_INSTALL/SAWS/SAWS.py
```
* Reboot
