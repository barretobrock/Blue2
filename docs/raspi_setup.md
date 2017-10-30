# Raspberry Pi Setup

1. [Changing Locale/Timezone](#locale_timezone)
    1. []()
    1. []()
1. []()


## Changing Locale/Timezone <a id="locale_timezone"></a>
1. Configure locales
```bash
sudo dpkg-reconfigure locales
```
If perl warning about falling back to standard locale ("C"), do the following:
```bash
# Open the locale file
sudo nano /etc/default/locale
# Put the following lines in the file and save
LANG=en_US.UTF-8
LANGUAGE=en_US.UTF-8
LC_CTYPE=en_US.UTF-8
LC_NUMERIC=en_US.UTF-8
LC_TIME=en_US.UTF-8
LC_COLLATE=en_US.UTF-8
LC_MONETARY=en_US.UTF-8
LC_MESSAGES=en_US.UTF-8
LC_PAPER=en_US.UTF-8
LC_NAME=en_US.UTF-8
LC_ADDRESS=en_US.UTF-8
LC_TELEPHONE=en_US.UTF-8
LC_MEASUREMENT=en_US.UTF-8
LC_IDENTIFICATION=en_US.UTF-8
LC_ALL=en_US.UTF-8
```

2. Set the keyboard layout
```bash
sudo dpkg-reconfigure keyboard-configuration
```
3. Set the timezone
```bash
sudo dpkg-reconfigure tzdata
```
4. Update lists and reboot
```bash
sudo apt-get update
sudo reboot
```
