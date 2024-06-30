# sensor-library-python
Unified sensor library is a wrapper around various type of sensor lib for raspberry pi

### install 

```

sudo pip3 install -r requirements.txt --break-system-packages"

```


## Example usage 

```python

from sensor_lib.main import create_sensor
sensor = create_sensor('dht11', {"pin_no":14})
data = sensor.read()
print(data) # Example output: {'humidity': 67.0, 'temperature': 33.0}

```
