# Python app

If you encounter any problems running program, please open a new issue. Also, please consider opening an issue if you have any questions or suggestions for improving the installation process.

Code is compatible with Python 3.7.

```
pip install -r requirements.txt
conda install --file requirements.txt
```


# CROSS COMPATIBILITY STUFF
# - Passer sur audiodevice par rapport a pyaudio

## Deploy on raspberrypi

For Raspberry Pi it has been tested on Raspberry 4, the 4go ram version.
On Debian Buster.

Here are some conf file you can add to your debian mounted sd card to automate wifi and ssh stuff.

### Wifi automation

wpa_supplicant.conf

'
country=US # Your 2-digit country code
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
'

### SSH auto enabling

touch ssh


## Installation

git clone http://github.com/tfrere/music-to-led
pip3 install -r requirements.txt
pip3 install mido
sudo apt-get install python3-pyaudio
sudo apt-get install python3-rtmidi
sudo apt-get install libatlas-base-dev
sudo apt-get install python3-numpy
