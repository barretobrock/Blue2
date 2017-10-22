# Blue2
A directory of scripts for every function from home automation to web-scraping. 

## Requirements
### Python Version
    As of now, most files are tested using primarily Python 3.4 (for Raspbian distro)

### Static IP
    Not really a requirement, but it definitely makes it easier if you set the pi's IP address to be static.
    Steps include:
        1.) Reserving the pi's static IP address with your router
        2.) Set the pi's static address [here's a good place to start](https://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address)

### [Passwordless SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md)
    Set this up so the pi can connect to the server computer without having to use user password


### File Permissions
    Probably useful to give execute permissions to script
    `chmod a+x foo.py`

### Paramiko (File transfer through SCP)
    `sudo apt-get install python3-paramiko`
    `sudo pip3 install scp`

### pushbullet
    `sudo pip3 install pushbullet.py`

### pandas (installed on home server computer, for now)
    `sudo apt-get install python3-pandas`

### Plotly
    `sudo pip3 install plotly`

### Google Client Library and support modules (installed on home server computer for now)
    `sudo pip3 install --upgrade google-api-python-client`
    'sudo pip3 install gspread oauth2client'
    - Follow instructions from [this link](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

### wireless (WIFI connection, scanner)
    ```
    # Preliminary update of setuptools may be necessary
    sudo pip3 install --upgrade setuptools

    sudo pip3 install wireless
    ```
### OBD2
    ```
    # Make sure python-dev or python3-dev are installed
    sudo apt-get install python3-dev
    sudo apt-get install libbluetooth-dev

    # Check connection to bluetooth device
    # In shell:
    sudo bluetoothctl
    power on
    agent on
    pairable on
    scan on # Scan for devices, get MAC address
    scan off
    pair <mac_address>
    # You may need to enter PIN at this point
    trust <mac_address>
    connect <mac_address>
    quit

    # Using OBD package
    # Bind bluetooth device to rfcomm0
    sudo rfcomm bind rfcomm0 <dev_mac_address>

    # Upgrade pyserial
    # First, find current serial version
    python
    import serial
    serial.VERSION
    quit()
    # Then, update it
    sudo pip install --upgrade pyserial

    ```

## Troubleshooting

### Crontab logs
    `/var/log/syslog`



## Structure
As some scripts will attempt to pull or save information to certain directories, a certain uniform structure is needed to make reusing scripts throughout different projects easy and fast. Collected data, logs and other information that should not be stored on the repo are kept in separate directories. The expected structure is shown below:
```
~/
└───/blue2
│   └───/camera
│   └───/comm
│   └───/primary
│   └───/logging
│   └───/sensors
│   │   └───/temp
│   │   └───/light
│   │   └───/sound
│   └───/setup
│   └───/signals
│   └───/switches
│   └───/weather
└───/keys
└───/logs
└───/data
```
  
