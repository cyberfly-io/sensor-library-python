# sensor-library-python
Unified sensor library is a wrapper around various type of sensor lib for raspberry pi

### install 

for raspberry pi 4

```
sudo pip3 install -r requirements.txt
```

for raspberry pi 5

```

sudo pip3 install -r requirements.txt --break-system-packages

```

Enable I2C interface for BMP280/MPU6050 sensors

```
sudo raspi-config
```

### DHT11 Temperature sensor 

```python

from sensor_lib.main import create_sensor
sensor = create_sensor('dht11', {"pin_no":14})
data = sensor.read()
print(data) # Example output: {'humidity': 67.0, 'temperature': 33.0}

```

### PIR motion sensor

```python

from sensor_lib.main import create_sensor
sensor = create_sensor('pir', {"pin_no":4})
def motion():
   print("motion detected")
sensor.pir.when_motion = motion
while 1:
    pass
```

### BMP280 temperature, pressure, altitude sensor

```python
from sensor_lib.main import create_sensor
import time
sensor = create_sensor('bmp280', {"address":0x76}) # 0x77 is default if address is not provided


while 1:
    print(sensor.read())
    time.sleep(2)
```

### MPU6050 sensor

```python
from sensor_lib.main import create_sensor
import time
sensor = create_sensor('mpu6050', {"address":0x68})


while 1:
    print(sensor.read())
    time.sleep(2)
```

### Digital Input

```python
from sensor_lib.main import create_sensor
import time
sensor = create_sensor('din', {"pin_no":17})
while 1:
    print(sensor.read())
    time.sleep(2)
```

### Hall effect

```python
from sensor_lib.main import create_sensor
import time
sensor = create_sensor('hall', {"pin_no":17})


while 1:
    print(sensor.read())
    time.sleep(2)
```

### Digital Output

```python
from sensor_lib.main import create_sensor
import time
sensor = create_sensor('dout', {"pin_no":4})

sensor.device.on()

while 1:
    pass
```
