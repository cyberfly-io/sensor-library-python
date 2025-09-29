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
| `bme680` | Bosch BME680 environmental sensor with gas resistance. | Optional `address` (default `0x77`), optional `sea_level_pressure`, optional `i2c_bus`. | `{"temperature": °C, "humidity": %, "pressure": hPa, "gas": ohms}` |
| `ccs811` | AMS CCS811 air quality sensor for equivalent CO₂ and TVOC. | Optional `address` (default `0x5A`), optional `temperature_offset`, optional `baseline`, optional `i2c_bus`. | `{"eco2": ppm, "tvoc": ppb, "temperature": °C, "baseline": int}` |
| `vl53l0x` | ST VL53L0X time-of-flight distance sensor. | Optional `address` (default `0x29`), optional `measurement_timing_budget`, optional `signal_rate_limit`, optional `i2c_bus`. | `{"distance_mm": mm, "distance_cm": cm}` |
| `ads1115` | Analog-to-digital converter for 4 single-ended inputs. | Optional `address` (default `0x48`), optional `channel`, optional `gain`, optional `data_rate`, optional `i2c_bus`. | `{"channel": index, "raw": value, "voltage": volts, "gain": gain}` |
| `mpu6050` | 6-axis accelerometer + gyroscope (MPU6050). | Optional `address` (default `0x68`), optional `i2c_bus`. | `{"acceleration": {x,y,z}, "gyro": {x,y,z}, "temperature": °C}` |
| `hc_sr04` | HC-SR04 ultrasonic distance measurement. | `trigger_pin`, `echo_pin`, optional `max_distance`, optional `threshold_distance`. | `{"distance_m": meters, "is_within_threshold": bool}` |
| `ds18b20` | Waterproof 1-Wire temperature probe (DS18B20). | Optional `sensor_id`, optional `unit` (`celsius`/`fahrenheit`/`kelvin`). | `{"temperature": value, "unit": unit}` |
| `sht31d` | Sensirion SHT31-D temperature and humidity sensor. | Optional `address` (default `0x44`), optional `heater`, optional `i2c_bus`. | `{"temperature": °C, "humidity": %, "heater": bool}` |
| `tcs34725` | TCS34725 RGB color sensor with IR filter. | Optional `address` (default `0x29`), optional `gain`, optional `integration_time`, optional `i2c_bus`. | `{"raw": {"red": int, ...}, "rgb": {"r": int, ...}, "lux": float, "color_temperature": K}` |


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

## Supported display modules

| Key | Purpose | Inputs | Output payload |
| --- | --- | --- | --- |
| `lcd1602` | 16x2 HD44780-compatible I2C LCD for messages. | Optional `address` (default `0x27`), optional `columns`, optional `rows`, optional `text`, optional `auto_linebreaks`, optional `i2c_bus`. | `{"text": last_displayed}` |
| `ht16k33` | HT16K33 4-character alphanumeric/7-segment display. | Optional `address` (default `0x70`), optional `text`, optional `align_right`, optional `i2c_bus`. | `{"text": last_displayed}` |

### BME680 gas, humidity, pressure & temperature sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('bme680', {"address": 0x77, "sea_level_pressure": 1013.25})

while True:
    reading = sensor.read()
    print(
        "Temp: {0:.1f}°C  Humidity: {1:.1f}%  Pressure: {2:.1f} hPa  Gas: {3:.0f} Ω".format(
            reading['temperature'], reading['humidity'], reading['pressure'], reading['gas']
        )
    )
    time.sleep(2)
```

### CCS811 air quality sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('ccs811', {"address": 0x5A, "temperature_offset": -2.0})

while True:
    reading = sensor.read()
    print(
        "eCO₂: {0:.0f} ppm  TVOC: {1:.0f} ppb  Temp: {2:.1f}°C".format(
            reading['eco2'], reading['tvoc'], reading['temperature']
        )
    )
    time.sleep(1)
```

### VL53L0X time-of-flight distance sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('vl53l0x', {"measurement_timing_budget": 50000})

while True:
    reading = sensor.read()
    print(f"Distance: {reading['distance_mm']} mm ({reading['distance_cm']:.1f} cm)")
    time.sleep(0.2)
```

### ADS1115 4-channel ADC

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('ads1115', {"channel": 0, "gain": 1, "data_rate": 128})

while True:
    reading = sensor.read()
    print(
        "Channel {0}: raw={1} voltage={2:.4f} V (gain={3})".format(
            reading['channel'], reading['raw'], reading['voltage'], reading['gain']
        )
    )
    time.sleep(0.5)
```

### LCD1602 I2C character display

```python
from sensor_lib.main import create_sensor
import time

lcd = create_sensor('lcd1602', {"text": "Booting..."})

# Update both lines (use "\n" for line breaks)
lcd.display_text("Hello!\nTemp 24°C")
time.sleep(2)

# Append without clearing the screen
lcd.append_text("*")

print(lcd.read())  # {'text': 'Hello!\nTemp 24°C*'}

time.sleep(5)
lcd.clear()
```

### HT16K33 7-segment display

```python
from sensor_lib.main import create_sensor
import time
import datetime

display = create_sensor('ht16k33', {"align_right": True})

while True:
    now = datetime.datetime.now()
    display.display_text(now.strftime("%H%M"))
    time.sleep(1)
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

### DS18B20 1-Wire temperature sensor

```python
from sensor_lib.main import create_sensor
import time

# Optional: specify sensor_id if multiple probes are connected
sensor = create_sensor('ds18b20', {"unit": "celsius"})

while True:
    reading = sensor.read()
    print(f"Temperature: {reading['temperature']:.2f}° {reading['unit'][0].upper()}")
    time.sleep(2)
```

### SHT31-D temperature & humidity sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('sht31d', {"heater": False})

while True:
    reading = sensor.read()
    print(
        f"Temp: {reading['temperature']:.1f}°C  Humidity: {reading['humidity']:.1f}%  Heater: {reading['heater']}"
    )
    time.sleep(2)
```

### TCS34725 RGB color sensor

```python
from sensor_lib.main import create_sensor
import time

sensor = create_sensor('tcs34725', {"gain": "GAIN_4X"})

while True:
    reading = sensor.read()
    rgb = reading['rgb']
    print(
        "RGB: ({r}, {g}, {b})  Lux: {lux:.1f}  CCT: {cct:.0f}K".format(
            r=rgb['r'], g=rgb['g'], b=rgb['b'],
            lux=reading.get('lux', 0.0),
            cct=reading.get('color_temperature', 0.0)
        )
    )
    time.sleep(1)
```
