from socket import socket, AF_INET, SOCK_DGRAM
from Adafruit_ADXL345 import ADXL345
from time import sleep
from backend.config import (
    UDP_RECEIVER, 
    UDP_PATIENT_ID, 
    FALL_CONFIDENCE
)

adxl = ADXL345()
sock = socket(AF_INET, SOCK_DGRAM)

def main():
    while True:
        x, y, z = adxl.read() 
        total_fall = abs(z) + abs(x) + abs(y)
    
        if total_fall > FALL_CONFIDENCE:
            sock.sendto(bytes(f'[{UDP_PATIENT_ID}] Fall detected...', 'utf-8'), 
                        (UDP_RECEIVER, UDP_PATIENT_ID))
            sleep(2)

        total_fall = 0

if __name__ == "__main__":
    main()