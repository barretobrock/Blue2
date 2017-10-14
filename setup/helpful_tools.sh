#!/usr/bin/env bash

### NETWORK TOOLS
# Lookup all IPs in LAN
sudo nmap -sP 10.0.1.0/24
# Scan ports at IP
nmap 10.0.1.11
# Scan for OS and Services
nmap -A 10.0.1.11

