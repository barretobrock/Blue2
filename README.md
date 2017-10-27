# Blue2
A directory of scripts for functions from home automation to web-scraping.

## Requirements
### Python Version
As of now, most files are tested using primarily Python 3.4+ (for Raspbian distro & Xubuntu)

### Static IP
Not really a requirement, but it definitely makes it easier if you set the pi's IP address to be static.
Steps include:
    1.) Reserving the pi's static IP address with your router
    2.) Set the pi's static address here's a [good place to start](https://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address)

Example:
```bash
allow-hotplug wlan0
iface wlan0 inet static
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
    address 192.168.0.X
    netmask 255.255.255.0
    network 192.168.0.0
    broadcast 192.168.0.255
    gateway 192.168.0.1
```


### [Passwordless SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md)
Set this up so the pi can connect to the server computer without having to use user password

### File Permissions
Probably useful to give execute permissions to script
```bash
chmod a+x foo.py
```

### Paramiko (File transfer through SCP)
```bash
sudo apt-get install python3-paramiko
```

### Pushbullet
```bash
sudo pip3 install pushbullet.py
```

### Pandas
```bash
sudo apt-get install python3-pandas
```

### Plotly
```bash
sudo pip3 install plotly
```

### Google Client Library and support modules (installed on home server computer for now)
Follow instructions from [this link](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
```bash
sudo pip3 install --upgrade google-api-python-client
sudo pip3 install gspread oauth2client
```

### OBD2
```bash
# Make sure python-dev or python3-dev are installed
sudo apt-get install python3-dev
sudo apt-get install libbluetooth-dev

# Check connection to bluetooth device
# In shell:
sudo bluetoothctl
> power on
> agent on
> pairable on
> scan on # Scan for devices, get MAC address
> scan off
> pair <mac_address>
# You may need to enter PIN at this point
> trust <mac_address>
> connect <mac_address>
> quit

# Using OBD package
# Bind bluetooth device to rfcomm0
sudo rfcomm bind rfcomm0 <dev_mac_address>
# Put this command in the following file:
sudo nano .bashrc
```
```python
# Upgrade pyserial
# First, find current serial version

import serial
serial.VERSION
quit()
```
```bash
# Then, update it
sudo pip install --upgrade pyserial
```

## Troubleshooting

### Git highlighter
Always useful for determining which branch you're on!
Found in setup/git_highlighter.sh

### Crontab logs
```bash
/var/log/syslog
```

## Structure
As some scripts will attempt to pull or save information to certain directories, a certain uniform structure is needed to make reusing scripts throughout different projects easy and fast. Collected data, logs and other information that should not be stored on the repo are kept in separate directories. The expected structure is shown below:
```
~/
└───/blue2
│   └───/agg    
│   └───/camera
│   └───/comm
│   └───/logging
│   └───/primary
│   └───/sensors
│   │   └───/temp
│   │   └───/light
│   │   └───/sound
│   └───/setup
│   └───/signals
│   └───/switches
│   └───/weather
└───/data
└───/keys
└───/logs
```
  
