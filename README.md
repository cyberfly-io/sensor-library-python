# sensor-library-python
Unified sensor library is a wrapper around various type of sensor lib for raspberry pi

### install 

for raspberry pi 4

```
sudo pip3 install -r requirements.txt
```


for raspberry pi 5

```

sudo pip3 install -r requirements.txt --break-system-packages"

```


## DHT11 Temperature sensor 

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
