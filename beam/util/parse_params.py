import argparse

def parse():
    parser = argparse.ArgumentParser(prog="beam")
    parser.add_argument("-v", "--verbose", action="count", default=0, dest="verbose")

    subparser = parser.add_subparsers(dest="command", required=True)
    connectp = subparser.add_parser("connect", help="Connect to a specified connection")
    addp = subparser.add_parser("add", help="Add a connection to beam")
    removep = subparser.add_parser("remove", help="Remove a connection from beam")
    subparser.add_parser("list", help="Show all availabe connections")
    subparser.add_parser("version", help="Show the current version of beam")
    subparser.add_parser("help", help="Show help")

    connectp.add_argument("connection", help="One of the connection names that are shown with list")

    addp.add_argument("path", help="Path to the file to add")
    addp.add_argument("name", help="Custom name for connection")
    group2 = addp.add_mutually_exclusive_group(required=True)
    group2.add_argument("-wg", "--wireguard", action="store_true", help="Use Wireguard")
    group2.add_argument("-ovpn", "--openvpn", action="store_true", help="Use OpenVPN")

    removep.add_argument("name", help="Custom name of connection")

    return parser,parser.parse_args()