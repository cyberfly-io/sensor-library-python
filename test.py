from sensor_lib.main import create_sensor
import time
sensor = create_sensor('dht11', {"pin_no":14})
while 1:
    time.sleep(1)
    data = sensor.read()
    print(data) # Example output: {'humidity': 67.0, 'temperature': 33.0}