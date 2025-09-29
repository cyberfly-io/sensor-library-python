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

Enable I2C interface for BMP280/BME280/BH1750/MPU6050 sensors

```
sudo raspi-config
```

## Supported sensors

| Key | Purpose | Inputs | Output payload |
| --- | --- | --- | --- |
| `dht11` | Measure ambient temperature and humidity with inexpensive DHT11 module. | `pin_no` (GPIO). | `{"temperature": °C, "humidity": %}` |
| `pir` | Detect motion using a passive infrared sensor. | `pin_no` (GPIO). | `{"motion": bool, "value": 0/1}` |
| `din` | Read a generic digital input (e.g., button, reed switch). | `pin_no` (GPIO). | `{"input": 0/1}` |
| `hall` | Sense magnetic field for hall-effect switches. | `pin_no` (GPIO, pull-up enabled). | `{"magnet": bool}` |
| `water` | Detect water contact (rain / level sensor). | `pin_no` (GPIO). | `{"water": bool}` |
| `dout` | Drive a digital output or relay. | `pin_no` (GPIO), optional `active_high`, `initial_value`. | `{"output": bool}` |
| `vcgen` | Report Raspberry Pi CPU temperature via `vcgencmd`. | None. | `{"cpu_temperature": °C}` |
| `bmp280` | Bosch BMP280 barometric sensor for pressure/temperature/altitude. | Optional `address` (default `0x77`), optional `sea_level_pressure`, optional `i2c_bus`. | `{"temperature": °C, "pressure": hPa, "altitude": m}` |
| `bme280` | Bosch BME280 combined pressure, temperature, humidity sensor. | Optional `address` (default `0x77`), optional `sea_level_pressure`, optional `i2c_bus`. | `{"temperature": °C, "humidity": %, "pressure": hPa, "dew_point": °C}` |
| `bh1750` | BH1750 ambient light sensor for lux readings. | Optional `address` (default `0x23`), optional `i2c_bus`. | `{"illuminance": lux}` |
| `mpu6050` | 6-axis accelerometer + gyroscope (MPU6050). | Optional `address` (default `0x68`), optional `i2c_bus`. | `{"acceleration": {x,y,z}, "gyro": {x,y,z}, "temperature": °C}` |
| `hc_sr04` | HC-SR04 ultrasonic distance measurement. | `trigger_pin`, `echo_pin`, optional `max_distance`, optional `threshold_distance`. | `{"distance_m": meters, "is_within_threshold": bool}` |


### DHT11 temperature & humidity sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('dht11', {"pin_no": 14})

while True:
    reading = sensor.read()
    print(f"Temp: {reading['temperature']:.1f}°C  Humidity: {reading['humidity']:.1f}%")
    time.sleep(2)
```

### PIR motion sensor

```python
from sensor_lib.main import create_sensor

sensor = create_sensor('pir', {"pin_no": 4})

def motion_detected():
    print("motion detected!")

# Optional event callback exposed by gpiozero
sensor.pir.when_motion = motion_detected

while True:
    if sensor.read()["motion"]:
        motion_detected()
```

### VCGEN CPU temperature

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('vcgen', {})

while True:
    print(sensor.read())  # {'cpu_temperature': 48.7}
    time.sleep(5)
```

### BMP280 temperature, pressure & altitude sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('bmp280', {"address": 0x76})  # 0x77 is the default

while True:
    reading = sensor.read()
    print(reading)
    time.sleep(2)
```

### BME280 temperature, humidity & pressure sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('bme280', {"address": 0x76})

while True:
    print(sensor.read())
    time.sleep(2)
```

### BH1750 ambient light sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('bh1750', {"address": 0x23})

while True:
    lux = sensor.read()["illuminance"]
    print(f"Ambient light: {lux:.1f} lux")
    time.sleep(2)
```

### HC-SR04 ultrasonic distance sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('hc_sr04', {"trigger_pin": 23, "echo_pin": 24})

while True:
    reading = sensor.read()
    print(f"Distance: {reading['distance_m']*100:.1f} cm")
    time.sleep(0.5)
```

### MPU6050 6-DoF IMU sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('mpu6050', {"address": 0x68})

while True:
    reading = sensor.read()
    print(
        f"Accel: {reading['acceleration']}  Gyro: {reading['gyro']}  Temp: {reading['temperature']:.1f}°C"
    )
    time.sleep(1)
```

### Digital input (DIN)

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('din', {"pin_no": 17})

while True:
    print(sensor.read())
    time.sleep(0.5)
```

### Hall effect switch

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('hall', {"pin_no": 17})

while True:
    if sensor.read()["magnet"]:
        print("Magnet detected")
    time.sleep(0.5)
```

### Water level / rain sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('water', {"pin_no": 27})

while True:
    if sensor.read()["water"]:
        print("Water detected!")
    time.sleep(0.5)
```

### Digital output (DOUT)

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('dout', {"pin_no": 4, "initial_value": False})

while True:
    sensor.device.toggle()
    print(sensor.read())
    time.sleep(1)
```
