# justaphone
Simple Raspberry Pi Phone

# Notes
Should go with either the SIM7100a or the SIM7600a.  I'm not able to find one that comes already
soldered to a breakout.  I can find just the chip on Ebay or AliExpress.

You will need to enable SPI and hardware serial (pip install pyserial).

## Audio
If I order just the chip, maybe the audio breakout could work with a WT588D chip...?
See page 36 (section 3.6.2) of the SIM7000 hardware doc.

## SIM
docs say to protect it with an "ESD". Will need to figure out how to wire that in.

## Python
Waveshare 2.13v2 dipslay: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B)
Install python flask

To be able to shutdown as pi users via python: https://peppe8o.com/shutdown-button-with-raspberry-pi-and-python/

### setting the scripts to run at startup
Whever you desire, create an SH script like so:
```
cd /home/pi/justaphone/
#git pull > /home/pi/justaphone/gitupdate.log
git pull

cd /home/pi/justaphone/python/src
rm *.pyc
#python main.py > /home/pi/justaphone/python/phone.log
python main.py
```

Obviously, make sure to update directory paths.

Now let's setup crontab to run at boot.  Run
```
crontab -e
```

Add the following to the bottom of the file (update the path as needed!)
```
@reboot sudo sh /home/pi/justaphone/python/runme.sh > /home/pi/justaphone/python/runme.log &
```

The `runme.log` part is just in case you need to see what is going on in case of issues.

## Using Raspberry Pi Wavershare 5inch touchscreen
Link to the 5inch screen I'm using...you may need to do a calibration and such: https://www.waveshare.com/wiki/5inch_HDMI_LCD

I wanted to rotate the screen to be in portrait mode...the rotation of the screen was quick and easy but the touchscreen 
part was tricky.  Once you have the screen itself working, you'll want to do the following. Here is what worked for me:

Add the follwing to your `/boot/config.txt` (you'll need to use `sudo nano /boot/config.txt`) - this is what actually
rotates the screen 90deg.
```
display_rotate=1
```

Then to fix the touchscreen calibration, let's edit the calibration file.  To open in nano:
```
sudo nano /etc/X11/xorg.conf.d/99-calibration.conf
```

Here is a copy of mine....but you may need to tweak your numbers slightly with a calibration but hopefully this gets
you started.
```
Section "InputClass"
        Identifier      "calibration"
        MatchProduct    "ADS7846 Touchscreen"
        Option  "Calibration"   "3951 -59 3959 317"
        Option  "SwapAxes"      "0"
        Option "TransformationMatrix" "0 -1 1 1 0 0 0 0 1"
EndSection
```

You will need to do a reboot after this.

### Set URL to launch at start
```
sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
```

Add the following line to the file:
```
@chromium-browser --start-fullscreen --start-maximized http://localhost:5000/
```

The whole file should look something like this:
```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
#@xscreensaver -no-splash
@chromium-browser --start-fullscreen --start-maximized http://localhost:5000/
```

Notice the hash before the xscreensaver line...this may or may not be needed.

# Troubleshooting
Issues installing flask?  Checkout: https://stackoverflow.com/questions/46989508/install-flask-ask-on-raspberry-pi

# Icon link
https://www.copyandpastesymbols.net/telephone-symbol.html


