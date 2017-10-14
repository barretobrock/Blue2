# Blue2
A directory of scripts for every function from home automation to web-scraping. 

## Requirements
### pushbullet
  `pip install pushbullet.py`

## Structure
As some scripts will attempt to pull or save information to certain directories, a certain uniform structure is needed to make reusing scripts throughout different projects easy and fast. Collected data, logs and other information that should not be stored on the repo are kept in separate directories. The expected structure is shown below:
```
~/
└───/scripts *{BLUE2}*
│   └───/global
│   │   └───/main
│   └───/logging
│   └───/sensors
│   │   └───/temp
│   │   └───/light
│   │   └───/sound
│   └───/weather
│   └───/camera
└───/keys
└───/logs
└───/data
```
  
