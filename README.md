# Mock detector interface

This is a simple mock app to emulate the behaviour of a hardware detector when interfacing with the android sikorka app


## Installation

We need a Bluetooth enabled linux system with python 3.

Make sure bluetooth is activated and running -- guide may vary depending on your system -- for Arch check [here](https://wiki.archlinux.org/index.php/Bluetooth).

```
systemctl start bluetooth.service
```


If things don't work check this SO answer: https://stackoverflow.com/questions/33110992/python-code-for-bluetooth-throws-error-after-i-had-to-reset-the-adapter

Then create a python virtualenv and install the requirements:

```
pip install -r requirements.txt
```

## Connect to phone

To connect to your phone as a bluetooth device, have it open at the bluetooth settings and choose a unique device name for it.
Then from your terminal run the program with:

```
python main.py --devicename YOURDEVICENAMEHERE
```

## Run an RFCOM Bluetooth server

Make sure your device is up:

```
sudo hciconfig hci0 piscan
```

If the above gives you any errors, then make the interface go up by

```
sudo hciconfig hci0 up
```

Then provide a unique name for the device.

```
sudo hciconfig hci0 name 'Mock Detector'
```

And now run the server:

```
sudo python main.py
```

To connect to the server from your phone there are many ways. First of all open the bluetooth from your phone and pair with the
server. Should be either the name you gave above or `pybluez XX`.

We will use [blueterm](https://play.google.com/store/apps/details?id=es.pymasde.blueterm) a simple android app to play and debug bluetooth connections.

Open bluterm, click settings and connect to a device. From the paired devices you should find the mock detector. Connect to it. Then you can start typing and everything you type should be reflected in the server and depending on the server's configuration you can get something back. For example look at the screenshot below.

![Server](https://imgur.com/y1yEHXt)
![Client](https://imgur.com/Fv4Mz6K)


## Miscellaneous

Here are some nice tutorial on using python for bluetooth communication:

https://people.csail.mit.edu/albert/bluez-intro/c212.html
https://github.com/EnableTech/raspberry-bluetooth-demo
