from beam.util.parse_params import parse
from beam.util.log_level import DebugLevel
import sys
import importlib.metadata
import os
import pathlib
import shutil
import os
import subprocess
import time

home = pathlib.Path.home()
BEAM_FOLDER = home / pathlib.Path(".beam")
LOG_LEVEL = 0

def main():
    parser,args = parse()
    global LOG_LEVEL
    LOG_LEVEL = args.verbose
    log("Running beam programm", DebugLevel.EVERYTHING)
    init()
    match (args.command):
        case "connect":
            log("Connecting to VPN", DebugLevel.EVERYTHING)
            client = arg = "openvpn" if args.openvpn else "wireguard"
            connect(args.connection, client)
        case "version":
            log("Printing version information", DebugLevel.EVERYTHING)
            print(importlib.metadata.version("beam"))
        case "help":
            log("Printing help information", DebugLevel.EVERYTHING)
            parser.print_help()
        case "add":
            log("Trying to add VPN config", DebugLevel.EVERYTHING)
            add(args.path, args.name)
        case "remove":
            log("Trying to remove VPN config", DebugLevel.EVERYTHING)
            remove(args.name)
        case "list":
            log("Listing all possible VPN connections", DebugLevel.EVERYTHING)
            list_connections()

            

def init():
    log("Running init checks", DebugLevel.EVERYTHING)
    if not BEAM_FOLDER.is_dir():
        log(".beam folder not found. Creating it", DebugLevel.BASIC)
        BEAM_FOLDER.mkdir()

        

def add(path, name):
    log("Checking if file already exits", DebugLevel.EVERYTHING)
    from_path = pathlib.Path(path)
    to_path = BEAM_FOLDER / name
    if to_path.is_file():
        log("File already exists. Exiting")
        sys.exit()
    log("File will be added to beam", DebugLevel.BASIC)
    shutil.copy(from_path, to_path)
    log(f"Successfully added {from_path.name} to beam")
    


def remove(name):
    log("Checking if connection name is saved", DebugLevel.BASIC)
    for file in BEAM_FOLDER.iterdir():
        if file.stem == name:
            log(f"Connection found with name {name}", DebugLevel.EVERYTHING)
            file.unlink()
            log(f"Connection '{name}' removed")
            sys.exit()
    log(f"Connection '{name}' not found")
    


def list_connections():
    log("Going through all connections", DebugLevel.BASIC)
    print("--- CONNECTIONS ---")
    for file in BEAM_FOLDER.iterdir():
        print(f"- {file.stem}")


def connect(connection, client):
    match (client):
        case "openvpn":
            log("Using connection client OpenVPN", DebugLevel.BASIC)
            connect_to_openvpn(connection)
        case "wireguard":
            log("Using connection client Wireshark", DebugLevel.BASIC)
            connect_to_wireguard(connection)
                
        
def connect_to_openvpn(connection):
    log("Checking if connection name is saved", DebugLevel.BASIC)
    for file in BEAM_FOLDER.iterdir():
        if file.stem == connection:
            log(f"Connection found with name {connection}", DebugLevel.EVERYTHING)
            command = ["sudo", "openvpn", str(BEAM_FOLDER / file)]
            try:
                log("Connected to VPN Server")
                log("Press CTRL+C to close VPN connection")
                run_command(command)
            except subprocess.CalledProcessError as e:
                log("Could not connect to VPN Server")
            except KeyboardInterrupt:
                log("Disconnecting from VPN connection")
            sys.exit()
    log(f"Connection '{connection}' not found")

def connect_to_wireguard(connection):
    log("Checking if connection name is saved", DebugLevel.BASIC)
    for file in BEAM_FOLDER.iterdir():
        if file.stem == connection:
            log(f"Connection found with name {connection}", DebugLevel.EVERYTHING)
            command = ["sudo", "wg-quick", "up", str(BEAM_FOLDER / file)]
            try:
                run_command(command)
                log("Connected to VPN Server")
                log("Press CTRL+C to close VPN connection")
                log("")
                while True:
                    time.sleep(1)
            except subprocess.CalledProcessError as e:
                log("Could not connect to VPN Server")
            except KeyboardInterrupt:
                    log("Disconnecting from VPN connection")
                    command = ["sudo", "wg-quick", "down", str(BEAM_FOLDER / file)]
                    subprocess.run(command, check=True, text=True, capture_output=True)
            sys.exit()
    log(f"Connection '{connection}' not found")

def run_command(command):
    if LOG_LEVEL >= 1:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            for line in process.stdout:
                print(line, end='') 
    else:
        subprocess.run(command, check=True, text=True, capture_output=True)


def log(message, needed = DebugLevel.IMPORTANT):
    if LOG_LEVEL >= int(needed):
        print(f"\033[93m[!] {message}\033[0m")