

# <img src="https://user-images.githubusercontent.com/37932436/160900239-9d1b73ad-3840-43e6-83e9-905a5d43c4ed.png" width=50px height=50px\> beam

Beam is a in console VPN file manager. It works with OpenVPN as well as with Wireguard. (Wireguard currently untested)

---

## Installation
```bash
pipx install git+https://github.com/hydr0nium/beam.git
```

---

## Usage:
```
usage: beam [-h] [-v] {connect,add,remove,list,version,help} ...

positional arguments:
  {connect,add,remove,list,version,help}
    connect             Connect to a specified connection
    add                 Add a connection to beam
    remove              Remove a connection from beam
    list                Show all availabe connections
    version             Show the current version of beam
    help                Show help

options:
  -h, --help            show this help message and exit
  -v, --verbose
```
