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

## Connection

To connect to your phone as a bluetooth device, have it open at the bluetooth settings and choose a unique device name for it.
Then from your terminal run the program with:

```
python main.py --devicename YOURDEVICENAMEHERE
```

## Miscellaneous

Here are some nice tutorial on using python for bluetooth communication:

https://people.csail.mit.edu/albert/bluez-intro/c212.html
