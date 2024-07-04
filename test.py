from sensor_lib.main import create_sensor
import time
sensor = create_sensor('mpu6050', {"address":0x68})


while 1:
    print(sensor.read())
    time.sleep(2)
