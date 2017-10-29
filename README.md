# Blue2
A collection of scripts that make it easier for me to do stuff.
Projects include, but are not limited to:
- Work <-> home commute calculator
- Car engine data recorder

## Table of Contents
1. [Requirements](#requirements)
    1. [Python Version](#python_version)
    1. [Static IP](#static_ip)
    1. [Passwordless SSH](#passwordless_ssh)
    1. [File Permissions](#file_permissions)
    1. [Python Packages](#python_packages)
        1. [Paramiko](#paramiko)
        1. [Pushbullet](#pushbullet)
        1. [Pandas](#pandas)
        1. [Plotly](#plotly)
        1. [Google Client Library](#google_client_library)
        1. [OBD2 for Python](#python-obd)
    1. [OBD over Bluetooth](#obd_setup)
1. [Tools](#tools)
    1. [Git Highlighter](#git_highlighter)
1. [Troubleshooting](#troubleshooting)
    1. [Accessing Crontab logs](#crontab_logs)
1. [Crontab Tasks](#crontab_tasks)
1. [Repo Structure](#structure)

## Requirements <a id="requirements"></a>
### Python Version <a id="python_version"></a>
As of now, most files are tested using primarily Python 3.4+ (tested on Raspbian & Xubuntu distros)

### Static IP <a id="static_ip"></a>
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


### [Passwordless SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md) <a id="passwordless_ssh"></a>
Set this up so the pi can connect to the server computer without having to use user password

- Check that the RasPi has a `.ssh` folder. If not, make one:
```bash
cd ~
install -d -m 700 ~/.ssh
```
- Generate a new key for connecting to the specific computer
```bash
ssh-keygen -t rsa -C <USERNAME>@<HOSTNAME>

# Press <Enter> 3x

# Copy public key to target computer
cat ~/.ssh/id_rsa.pub | ssh <USERNAME>@<IP_ADDRESS> 'cat >> .ssh/authorized_keys'
```

### File Permissions <a id="file_permissions"></a>
Probably useful to give execute permissions to script
```bash
chmod a+x foo.py
```

### Python Packages <a id="python_packages"></a>
#### Paramiko (File transfer through SCP) <a id="paramiko"></a>
```bash
sudo apt-get install python3-paramiko
```

#### Pushbullet <a id="pushbullet"></a>
```bash
sudo pip3 install pushbullet.py
```

#### Pandas <a id="pandas"></a>
```bash
sudo apt-get install python3-pandas
```

#### Plotly <a id="plotly"></a>
```bash
sudo pip3 install plotly
```

#### Google Client Library and support modules (installed on home server computer for now) <a id="google_client_library"></a>
Follow instructions from [this link](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
```bash
sudo pip3 install --upgrade google-api-python-client
sudo pip3 install gspread oauth2client
```

#### python-obd <a id="obd2"></a>
```bash
sudo pip3 install obd
```

### OBD Over Bluetooth Setup <a id="obd_setup"></a>
```bash
# Make sure python-dev or python3-dev are installed
sudo apt-get install python3-dev libbluetooth-dev
sudo pip3 install obd

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
sudo pip3 install --upgrade pyserial
```

## Tools <a id="tools"></a>
### Git highlighter <a id="git_highlighter"></a>
Always useful for determining which git branch you're on!
Found in [setup/git_highlighter.sh](setup/git_highlighter.sh)

## Troubleshooting <a id="troubleshooting"></a>

### Access crontab logs <a id="crontab_logs"></a>
```bash
/var/log/syslog
```

## Crontab Tasks <a id="crontab_tasks"></a>

#### Home Server
```
*/5 * * * * /usr/bin/python3 ~/blue2/weather/severe_weather_check.py
*/10 07-20 * * 1-5 /usr/bin/python3 ~/blue2/comm/commute_calc.py
10 0 * * * /usr/bin/python3 ~/blue2/agg/obd_compacter.py
```
#### autoPi
```
*/5 * * * * /usr/bin/python3 ~/blue2/sensors/honda_obd.py
0 0 * * * /usr/bin/python3 ~/blue2/comm/obd_scp.py
```

## Structure <a id="structure"></a>
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
│   └───/setup
│   └───/signals
│   └───/switches
│   └───/weather
└───/data
└───/keys
└───/logs
```
  
