# Blue2
A directory of scripts for every function from home automation to web-scraping. 

## Requirements
### Python Version
    As of now, most files are tested using primarily Python 3.4 (for Raspbian distro)

### File Permissions
    Probably useful to give execute permissions to script
    `chmod a+x foo.py`

### pushbullet
    `sudo pip3 install pushbullet.py`

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
  
