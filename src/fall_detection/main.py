from socket import socket, AF_INET, SOCK_DGRAM
from Adafruit_ADXL345 import ADXL345
from time import sleep
from settings import UDP_IP, UDP_PORT, FALL_CONFIDENCE

adxl = ADXL345()
sock = socket(AF_INET, SOCK_DGRAM)

while True:
    x, y, z = adxl.read() 
    total_fall = abs(z) + abs(x) + abs(y)
 
    if total_fall > FALL_CONFIDENCE:
        sock.sendto(bytes("FALL DETECTED", 'utf-8'), 
                    (UDP_IP, UDP_PORT))
        sleep(2)

    total_fall = 0