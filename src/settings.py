from dotenv import load_dotenv
import os

load_dotenv()

FALL_CONFIDENCE: os.getenv('FALL_CONFIDENCE')
UDP_IP: os.getenv('UDP_IP')
UDP_PORT: os.getenv('UDP_PORT')


