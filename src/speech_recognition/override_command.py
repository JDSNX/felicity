import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep
from backend.config import (
  settings, logger
)
 

def update_sql(app, execute, isOpen):
    """
    To be change to SQLAlchemy
    """
    # conn = pyodbc.connect('DRIVER=FreeTDS;'
    #   'SERVER=192.168.1.13;'
    #   'PORT=1433;'
    #   'DATABASE=EPMAtry;'
    #   'UID=epma;'
    #   'PWD=epma;'
    #   'TDS_Version=8.0;')
    #   cursor = conn.cursor()
    #   #print(execute)
    #   #print(app)
    #   cursor.execute('''
    #   UPDATE dbo.ROOMS set ''' + app + ''' = ?, ''' + execute + ''' = ?
    #   WHERE PatientID = ? AND RoomNo = ?''',(isOpen, 0, PatientID, PatientRoom))
    # conn.commit()
    pass

def set_gpio():
    logger.info('Initializing GPIO...')
  
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings.pin_light, GPIO.OUT)
    GPIO.setup(settings.pin_door, GPIO.OUT)
    GPIO.setup(settings.pin_window, GPIO.OUT)
    
    GPIO.output(settings.pin_light, True)
    GPIO.output(settings.pin_door, True)
    GPIO.output(settings.pin_window, False)
  
    logger.info('Initializing complete...')
 
def execute_gpio(PIN, state):
    GPIO.output(PIN, state)
 
def ServoCycle(CW_SERVO):
    i = 0
    servo = Servo(settings.pin_window)
    if CW_SERVO:
        while i != 72:
          servo.min()
          sleep(0.5)
          i+=1
    else:
        while i != 80:
          servo.max()
          sleep(0.5)
          i+=1

if __name__ == '__main__':
    set_gpio()

    while True:
        """
        WIP
        Code will be change according to SQLAlchemy
        """
        # conn = pyodbc.connect('DRIVER=FreeTDS;'
        # 'SERVER=192.168.1.13;'
        # 'PORT=1433;'
        # 'DATABASE=EPMAtry;'
        # 'UID=epma;'
        # 327 | Page
        # 'PWD=epma;'
        # 'TDS_Version=8.0;')
        # cursor = conn.cursor()
        # cursor.execute('''
        # SELECT light, window, door, isExecuteDoor, isExecuteLight, isExecuteWindow
        # FROM dbo.ROOMS
        # WHERE PatientID = ? AND RoomNo = ?''',(PatientID, PatientRoom))
        
        # for row in cursor:
        #   isLights = row.isExecuteLight
        #   isDoor = row.isExecuteDoor
        #   isWindow = row.isExecuteWindow
        
        # if isLights: 
        #   if settings.light:
        #     execute_gpio(PIN_LIGHT, True)
        #     update_sql('light', 'isExecuteLight', 0)
        #     settings.light = False
        #   else:
        #     execute_gpio(PIN_LIGHT, False)
        #     update_sql('light', 'isExecuteLight', 1)
        #     settings.light = True
        # elif isDoor:
        #   if settings.door:
        #     execute_gpio(PIN_DOOR, True)
        #     update_sql('door', 'isExecuteDoor', 0)
        #     settings.door = False
        #   else:
        #     execute_gpio(PIN_DOOR, False)
        #     update_sql('door', 'isExecuteDoor', 1)
        #     settings.door = True
        # elif isWindow:
        #   if settings.window:
        #     update_sql('window', 'isExecuteWindow', 0)
        #     ServoCycle(False)
        #     settings.window = False
        #   else:
        #     update_sql('window', 'isExecuteWindow', 1)
        #     ServoCycle(True)
        #     settings.window = True
