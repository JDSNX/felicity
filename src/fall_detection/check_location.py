import subprocess
import time
import re 
import pyodbc
import socket

from socket import socket, AF_INET, SOCK_DGRAM
from argparse import ArgumentParser
from schemas import Location
from settings import (
    logger, 
    UDP_RECEIVER, 
    UDP_FROM_SERVER, 
    UDP_PATIENT_ID,
    ROOM_NUMBER
)

parser = ArgumentParser(description='Display WLAN signal strength.')
parser.add_argument(
    dest='interface', 
    nargs='?', 
    default='wlan0', 
    help='wlan interface (default: wlan0)'
)

args = parser.parse_args()
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((UDP_FROM_SERVER, UDP_PATIENT_ID))


def update_fall(location, room): 
    conn = pyodbc.connect('DRIVER=FreeTDS;'
                        'SERVER=192.168.1.13;'
                        'PORT=1433;'
                        'DATABASE=EPMAtry;'
                        'UID=epma;'
                        'PWD=epma;'
                        'TDS_Version=8.0;')
    cursor = conn.cursor()
 
    if location == Location.LIVING_ROOM:
        cursor.execute('''
        UPDATE pi
        SET pi.isFall = 1, pi.isLocation = 1
        FROM dbo.PATIENT_INFORMATION pi JOIN dbo.ROOMS ro on ro.PatientID = pi.PatientID
        WHERE ro.RoomNo = ? AND pi.RoomNo = ?''',(room, room))
    elif location == Location.COMFORT_ROOM:
        cursor.execute('''
        UPDATE pi
        SET pi.isFall = 1, pi.isLocation = 0
        FROM dbo.PATIENT_INFORMATION pi JOIN dbo.ROOMS ro on ro.PatientID = pi.PatientID
        WHERE ro.RoomNo = ? AND pi.RoomNo = ?''',(room, room))

    conn.commit()

def main():
    while True: 
        logger.info('READY...')
        data, addr = sock.recvfrom(1024)
        cmd = subprocess.Popen('iwconfig %s' % args.interface, shell=True,stdout=subprocess.PIPE)

        for line in cmd.stdout: 
            if 'Link Quality' in line:
                check_map = list(map(int, re.findall(r'\d+', line)))

                if check_map[2] <= 50:
                    update_fall(Location.COMFORT_ROOM, ROOM_NUMBER)
                    sock.sendto(f"COMFORT ROOM #{ROOM_NUMBER}", (UDP_RECEIVER, UDP_PATIENT_ID))

                else:
                    update_fall(Location.COMFORT_ROOM, ROOM_NUMBER) 
                    sock.sendto(f"LIVING ROOM #{ROOM_NUMBER}", (UDP_RECEIVER, UDP_PATIENT_ID))

            elif 'Not-Asciated' in line:
                logger.info('NO SIGNAL')

if __name__ == "__main__":
    main()