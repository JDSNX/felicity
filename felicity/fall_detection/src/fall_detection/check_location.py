import subprocess
import re
import socket

from socket import socket, AF_INET, SOCK_DGRAM
from argparse import ArgumentParser
from schema import Location
from config import logger, settings

parser = ArgumentParser(description="Display WLAN signal strength.")
parser.add_argument(
    dest="interface", nargs="?", default="wlan0", help="wlan interface (default: wlan0)"
)

args = parser.parse_args()
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((settings.UDP_FROM_SERVER, settings.UDP_PATIENT_ID))


def update_fall(location, room):
    pass


def main():
    comfort_room_dist = 51  # Depends on how far the router
    # from the comfort_room

    while True:
        logger.info("READY...")
        cmd = subprocess.Popen(
            "iwconfig %s" % args.interface, shell=True, stdout=subprocess.PIPE
        )

        for line in cmd.stdout:
            if "Link Quality" in line:
                check_map = list(map(int, re.findall(r"\d+", line)))

                if check_map[2] < comfort_room_dist:
                    update_fall(Location.COMFORT_ROOM, settings.room_number)
                    sock.sendto(
                        f"COMFORT ROOM #{settings.room_number}",
                        (settings.UDP_RECEIVER, settings.UDP_PATIENT_ID),
                    )
                else:
                    update_fall(Location.LIVING_ROOM, settings.room_number)
                    sock.sendto(
                        f"LIVING ROOM #{settings.room_number}",
                        (settings.UDP_RECEIVER, settings.UDP_PATIENT_ID),
                    )

            elif "Not-Asciated" in line:
                logger.info("NO SIGNAL...")


if __name__ == "__main__":
    main()
