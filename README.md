# Blue2
A directory of scripts for every function from home automation to web-scraping. 

## Requirements
### pushbullet
    `pip install pushbullet.py`
### OBD2
    `pip install obd2`

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
  
