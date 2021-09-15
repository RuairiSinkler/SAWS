# Sinkler Automatic Weighing System
Python program to automatically control a hopper/augar system for mixing ingredents to be milled for chicken feed.

## Software Installation Instructions

### Main Setup
* Install latest version of Raspberry Pi OS onto Raspberry Pi (tested with Buster)
* Ensure you have Python 3.7 or later installed
* Install the openpyxl module with `sudo pip3 install openpyxl`
* Install PiJuice base with `sudo apt install pijuice-base`
* Clone this Github repository
* Run `sudo python3 SAWS/SAWS.py`

### Ensuring USB works correctly
* Ensure your USB is called "RATIONUSB" and copy rations.xlsx to it
* Plug in your USB and run `blkid` noting the UUID of your device (it will look something like `5C24-1453`)
* Run `sudo nano /etc/fstab` to edit the fstab file
* Add to the bottom: `UUID=*INSERT YOUR UUID HERE*  /mnt/RATIONUSB  vfat  defaults,nofail  0  0`
* Ensure the usb_location entry in config.ini matches this mount location (`/mnt/RATIONUSB`)

### To run at startup
#### Activate auto-login:
* Run Raspi-Config with `sudo raspi-config`
* Navigate to `3 Boot Options`
* Then `B1 Desktop / CLI`
* Finally select `B4 Desktop Autologin`
#### Run SAWS at Desktop Boot
* Ensure `~/.config/lxsession/LXDE-pi/autostart` exists
* Edit it with `nano ~/.config/lxsession/LXDE-pi/autostart`
* Ensure the file looks like this:
```
#@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
#@point-rpi
@/FULL_INSTALL_PATH/SAWS.sh
```
* Reboot
