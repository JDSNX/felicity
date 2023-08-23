from dotenv import load_dotenv
import os
import logging

logger = logging.basicConfig(level=logging.INFO)
load_dotenv()

FALL_CONFIDENCE: os.getenv('FALL_CONFIDENCE')
UDP_RECEIVER: os.getenv('UDP_RECEIVER')
UDP_PATIENT_ID: os.getenv('UDP_PATIENT_ID')
UDP_FROM_SERVER: os.getenv('UDP_FROM_SERVER')

ROOM_NUMBER: os.getenv('ROOM_NUMBER')

# PYODBC TO BE CHANGE TO SQLALCHEMY
DRIVER = os.getenv('DRIVER')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')
UID = os.getenv('UID')
PWD = os.getenv('PWD')
TDS_VERSION = os.getenv('TDS_VERSION')