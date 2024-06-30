from sensor_lib.main import create_sensor
import time
sensor = create_sensor('hall', {"pin_no":17})


while 1:
    print(sensor.read())
    time.sleep(2)
