# sensor-library-python
Unified sensor library for raspberry pi

## Example usage 

```python

from sensor_lib.main import create_sensor
sensor = create_sensor('dht11', {"pin_no":14})
data = sensor.read()
print(data) # Example output: {'humidity': 67.0, 'temperature': 33.0}

```
