from sensor_lib.main import create_sensor
import time
sensor = create_sensor('bmp280', {"address":0x76})


while 1:
    print(sensor.read())
    time.sleep(2)
