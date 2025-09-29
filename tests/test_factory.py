from __future__ import annotations

import sys
import types
import unittest

from sensor_lib.main import create_sensor


class FakeDHTModule(types.ModuleType):
    DHT11 = object()

    @staticmethod
    def read_retry(sensor, pin):
        return 55.5, 21.0


class FakeVcgencmd:
    def get_cpu_temp(self):
        return 48.75


class FakeDigitalInputDevice:
    def __init__(self, pin, pull_up=False):
        self.pin = pin
        self.pull_up = pull_up
        self.value = 0 if pull_up else 1


class FakeOutputDevice:
    def __init__(self, pin, active_high=True, initial_value=False):
        self.pin = pin
        self.active_high = active_high
        self.value = initial_value


class FakeMotionSensor:
    def __init__(self, pin):
        self.pin = pin
        self.when_motion = None
        self.motion_detected = True
        self.value = 1


class FakeDistanceSensor:
    def __init__(self, echo, trigger, max_distance=1.0, threshold_distance=0.3):
        self.echo = echo
        self.trigger = trigger
        self.max_distance = max_distance
        self.threshold_distance = threshold_distance
        self.distance = 0.25


class FakeBoard(types.ModuleType):
    def I2C(self):
        return object()


class FakeBMP280:
    def __init__(self, i2c, address=0x77):
        self.i2c = i2c
        self.address = address
        self.sea_level_pressure = 1013.25
        self.altitude = 123.4
        self.temperature = 22.5
        self.pressure = 990.0


class FakeBME280:
    def __init__(self, i2c, address=0x77):
        self.i2c = i2c
        self.address = address
        self.sea_level_pressure = 1013.25
        self.temperature = 21.9
        self.humidity = 43.0
        self.pressure = 1008.5
        self.dew_point = 10.2


class FakeBH1750:
    def __init__(self, i2c, address=0x23):
        self.i2c = i2c
        self.address = address
        self.lux = 123.0


class FakeBME680:
    def __init__(self, i2c, address=0x77):
        self.i2c = i2c
        self.address = address
        self.sea_level_pressure = 1013.25
        self.temperature = 23.4
        self.humidity = 42.0
        self.pressure = 1002.5
        self.gas = 1200.0


class FakeCCS811:
    def __init__(self, i2c, address=0x5A):
        self.i2c = i2c
        self.address = address
        self._temperature = 26.5
        self._temperature_offset = 0.0
        self._baseline = 0x1234
        self._eco2 = 415
        self._tvoc = 9
        self.data_ready = True

    @property
    def temperature_offset(self):
        return self._temperature_offset

    @temperature_offset.setter
    def temperature_offset(self, value):
        self._temperature_offset = float(value)

    @property
    def baseline(self):
        return self._baseline

    @baseline.setter
    def baseline(self, value):
        self._baseline = int(value)

    @property
    def temperature(self):
        return self._temperature + self._temperature_offset

    @property
    def eco2(self):
        return self._eco2

    @property
    def tvoc(self):
        return self._tvoc


class FakeADS1115:
    def __init__(self, i2c, address=0x48):
        self.i2c = i2c
        self.address = address
        self.gain = 1
        self.data_rate = 128


class FakeAnalogIn:
    def __init__(self, ads, pin):
        self.ads = ads
        self.pin = pin
        self.value = 21504
        self.voltage = 1.024


class FakeSHT31D:
    def __init__(self, i2c, address=0x44):
        self.i2c = i2c
        self.address = address
        self.temperature = 22.3
        self.relative_humidity = 40.5
        self.heater = False


class FakeCharacterLCD:
    def __init__(self, i2c, columns, rows, address=0x27):
        self.i2c = i2c
        self.columns = columns
        self.rows = rows
        self.address = address
        self.auto_linebreaks = True
        self.backlight = False
        self._message = ""

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = str(value)

    def clear(self):
        self._message = ""


class FakeSeg7x4:
    def __init__(self, i2c, address=0x70):
        self.i2c = i2c
        self.address = address
        self.buffer = "    "

    def fill(self, value):
        if value == 0:
            self.buffer = "    "

    def print(self, value):
        self.buffer = str(value)


class FakeTCS34725:
    GAIN_1X = 1
    GAIN_4X = 4
    GAIN_16X = 16
    GAIN_60X = 60

    INTEGRATIONTIME_2_4MS = 2.4
    INTEGRATIONTIME_24MS = 24
    INTEGRATIONTIME_50MS = 50

    def __init__(self, i2c, address=0x29):
        self.i2c = i2c
        self.address = address
        self.gain = self.GAIN_1X
        self.integration_time = self.INTEGRATIONTIME_2_4MS
        self.color_raw = (1024, 2048, 3072, 4096)
        self._rgb = (64, 96, 128)
        self.lux = 123.4
        self.color_temperature = 5100.0

    @property
    def color_rgb_bytes(self):
        return self._rgb


class FakeVL53L0X:
    def __init__(self, i2c, address=0x29):
        self.i2c = i2c
        self.address = address
        self._range = 512
        self._timing_budget = 200000
        self._signal_rate_limit = 0.25

    @property
    def range(self):
        return self._range

    @property
    def measurement_timing_budget(self):
        return self._timing_budget

    @measurement_timing_budget.setter
    def measurement_timing_budget(self, value):
        self._timing_budget = int(value)

    @property
    def signal_rate_limit(self):
        return self._signal_rate_limit

    @signal_rate_limit.setter
    def signal_rate_limit(self, value):
        self._signal_rate_limit = float(value)


class FakeMPU6050:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address
        self.acceleration = (1.0, 2.0, 3.0)
        self.gyro = (0.1, 0.2, 0.3)
        self.temperature = 24.5


class FakeW1ThermSensor:
    THERM_SENSOR_DS18B20 = 1
    DEGREES_C = 'celsius'
    DEGREES_F = 'fahrenheit'
    DEGREES_K = 'kelvin'

    def __init__(self, sensor_type=None, sensor_id=None):
        self.sensor_type = sensor_type
        self.sensor_id = sensor_id

    def get_temperature(self, unit):
        if unit == self.DEGREES_F:
            return 75.2
        if unit == self.DEGREES_K:
            return 295.0
        return 24.8


class SensorTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._original_modules = {}
        cls._install_fake_modules()

    @classmethod
    def tearDownClass(cls):
        for name, module in cls._original_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module

    @classmethod
    def _install_fake_modules(cls):
        def add_module(name, module):
            cls._original_modules.setdefault(name, sys.modules.get(name))
            sys.modules[name] = module

        add_module('Adafruit_DHT', FakeDHTModule('Adafruit_DHT'))

        vcgencmd_module = types.ModuleType('RaspberryPiVcgencmd')
        vcgencmd_module.Vcgencmd = FakeVcgencmd
        add_module('RaspberryPiVcgencmd', vcgencmd_module)

        gpiozero_module = types.ModuleType('gpiozero')
        gpiozero_module.DigitalInputDevice = FakeDigitalInputDevice
        gpiozero_module.OutputDevice = FakeOutputDevice
        gpiozero_module.MotionSensor = FakeMotionSensor
        gpiozero_module.DistanceSensor = FakeDistanceSensor
        add_module('gpiozero', gpiozero_module)

        board_module = FakeBoard('board')
        add_module('board', board_module)

        bmp_module = types.ModuleType('adafruit_bmp280')
        bmp_module.Adafruit_BMP280_I2C = FakeBMP280
        add_module('adafruit_bmp280', bmp_module)

        bme_module = types.ModuleType('adafruit_bme280')
        bme_module.Adafruit_BME280_I2C = FakeBME280
        add_module('adafruit_bme280', bme_module)

        bme680_module = types.ModuleType('adafruit_bme680')
        bme680_module.Adafruit_BME680_I2C = FakeBME680
        add_module('adafruit_bme680', bme680_module)

        ccs811_module = types.ModuleType('adafruit_ccs811')
        ccs811_module.CCS811 = FakeCCS811
        add_module('adafruit_ccs811', ccs811_module)

        ads_module = types.ModuleType('adafruit_ads1x15.ads1115')
        ads_module.ADS1115 = FakeADS1115
        ads_module.P0 = 0
        ads_module.P1 = 1
        ads_module.P2 = 2
        ads_module.P3 = 3
        add_module('adafruit_ads1x15.ads1115', ads_module)

        analog_module = types.ModuleType('adafruit_ads1x15.analog_in')
        analog_module.AnalogIn = FakeAnalogIn
        add_module('adafruit_ads1x15.analog_in', analog_module)

        sht_module = types.ModuleType('adafruit_sht31d')
        sht_module.SHT31D = FakeSHT31D
        add_module('adafruit_sht31d', sht_module)

        charlcd_pkg = types.ModuleType('adafruit_character_lcd')
        charlcd_i2c = types.ModuleType('adafruit_character_lcd.character_lcd_i2c')
        charlcd_i2c.Character_LCD_I2C = FakeCharacterLCD
        charlcd_pkg.character_lcd_i2c = charlcd_i2c
        add_module('adafruit_character_lcd', charlcd_pkg)
        add_module('adafruit_character_lcd.character_lcd_i2c', charlcd_i2c)

        ht16k33_pkg = types.ModuleType('adafruit_ht16k33')
        ht16k33_segments = types.ModuleType('adafruit_ht16k33.segments')
        ht16k33_segments.Seg7x4 = FakeSeg7x4
        ht16k33_pkg.segments = ht16k33_segments
        add_module('adafruit_ht16k33', ht16k33_pkg)
        add_module('adafruit_ht16k33.segments', ht16k33_segments)

        tcs_module = types.ModuleType('adafruit_tcs34725')
        tcs_module.TCS34725 = FakeTCS34725
        tcs_module.GAIN_1X = FakeTCS34725.GAIN_1X
        tcs_module.GAIN_4X = FakeTCS34725.GAIN_4X
        tcs_module.GAIN_16X = FakeTCS34725.GAIN_16X
        tcs_module.GAIN_60X = FakeTCS34725.GAIN_60X
        tcs_module.INTEGRATIONTIME_2_4MS = FakeTCS34725.INTEGRATIONTIME_2_4MS
        tcs_module.INTEGRATIONTIME_24MS = FakeTCS34725.INTEGRATIONTIME_24MS
        tcs_module.INTEGRATIONTIME_50MS = FakeTCS34725.INTEGRATIONTIME_50MS
        add_module('adafruit_tcs34725', tcs_module)

        vl53_module = types.ModuleType('adafruit_vl53l0x')
        vl53_module.VL53L0X = FakeVL53L0X
        add_module('adafruit_vl53l0x', vl53_module)

        bh_module = types.ModuleType('adafruit_bh1750')
        bh_module.AmbientLightSensor = FakeBH1750
        add_module('adafruit_bh1750', bh_module)

        mpu_module = types.ModuleType('adafruit_mpu6050')
        mpu_module.MPU6050 = FakeMPU6050
        add_module('adafruit_mpu6050', mpu_module)

        w1_module = types.ModuleType('w1thermsensor')
        w1_module.W1ThermSensor = FakeW1ThermSensor
        add_module('w1thermsensor', w1_module)

    def test_create_dht11(self):
        sensor = create_sensor('dht11', {"pin_no": 4})
        self.assertEqual(sensor.read(), {"humidity": 55.5, "temperature": 21.0})

    def test_bmp280_read(self):
        sensor = create_sensor('bmp280', {"address": 0x76})
        reading = sensor.read()
        self.assertIn('altitude', reading)
        self.assertEqual(reading['temperature'], 22.5)
        self.assertEqual(reading['pressure'], 990.0)

    def test_bme280_read(self):
        sensor = create_sensor('bme280', {})
        reading = sensor.read()
        self.assertIn('humidity', reading)
        self.assertEqual(reading['dew_point'], 10.2)

    def test_bme680_read(self):
        sensor = create_sensor('bme680', {"sea_level_pressure": 1020})
        reading = sensor.read()
        self.assertEqual(reading['temperature'], 23.4)
        self.assertEqual(reading['humidity'], 42.0)
        self.assertEqual(reading['pressure'], 1002.5)
        self.assertEqual(reading['gas'], 1200.0)

    def test_ccs811_read(self):
        sensor = create_sensor('ccs811', {"temperature_offset": 1.5, "baseline": 0x4567})
        reading = sensor.read()
        self.assertEqual(reading['eco2'], 415.0)
        self.assertEqual(reading['tvoc'], 9.0)
        self.assertAlmostEqual(reading['temperature'], 28.0)
        self.assertEqual(reading['baseline'], 0x4567)

    def test_ads1115_read(self):
        sensor = create_sensor('ads1115', {"channel": 2, "gain": 2, "data_rate": 250})
        reading = sensor.read()
        self.assertEqual(reading['channel'], 2)
        self.assertEqual(reading['raw'], 21504)
        self.assertAlmostEqual(reading['voltage'], 1.024)
        self.assertEqual(reading['gain'], 2)

    def test_lcd1602_display(self):
        lcd = create_sensor('lcd1602', {"text": "Hello"})
        self.assertEqual(lcd.read()['text'], 'Hello')

        lcd.display_text('Line1\nLine2')
        self.assertEqual(lcd.read()['text'], 'Line1\nLine2')

        lcd.append_text('!')
        self.assertEqual(lcd.read()['text'], 'Line1\nLine2!')

    def test_ht16k33_display(self):
        display = create_sensor('ht16k33', {"text": "INIT"})
        self.assertEqual(display.read()['text'], 'INIT')

        display.display_text('42', align_right=True)
        self.assertEqual(display.read()['text'], '  42')

    def test_vl53l0x_read(self):
        sensor = create_sensor('vl53l0x', {"measurement_timing_budget": 60000})
        reading = sensor.read()
        self.assertEqual(reading['distance_mm'], 512)
        self.assertAlmostEqual(reading['distance_cm'], 51.2)

    def test_bh1750_read(self):
        sensor = create_sensor('bh1750', {})
        self.assertEqual(sensor.read(), {"illuminance": 123.0})

    def test_hc_sr04_read(self):
        sensor = create_sensor('hc_sr04', {"trigger_pin": 23, "echo_pin": 24})
        reading = sensor.read()
        self.assertAlmostEqual(reading['distance_m'], 0.25)
        self.assertTrue(reading['is_within_threshold'])

    def test_dout_output(self):
        sensor = create_sensor('dout', {"pin_no": 5, "initial_value": True})
        self.assertTrue(sensor.read()['output'])

    def test_ds18b20_read(self):
        sensor = create_sensor('ds18b20', {"unit": "fahrenheit", "sensor_id": "28-00000"})
        reading = sensor.read()
        self.assertEqual(reading['unit'], 'fahrenheit')
        self.assertAlmostEqual(reading['temperature'], 75.2)

    def test_sht31d_read(self):
        sensor = create_sensor('sht31d', {"heater": True})
        reading = sensor.read()
        self.assertAlmostEqual(reading['temperature'], 22.3)
        self.assertAlmostEqual(reading['humidity'], 40.5)
        self.assertTrue(reading['heater'])

    def test_tcs34725_read(self):
        sensor = create_sensor('tcs34725', {"gain": "GAIN_16X", "integration_time": "INTEGRATIONTIME_24MS"})
        reading = sensor.read()
        self.assertEqual(reading['rgb'], {'r': 64, 'g': 96, 'b': 128})
        self.assertEqual(reading['raw']['red'], 1024)
        self.assertEqual(reading['gain'], FakeTCS34725.GAIN_16X)
        self.assertEqual(reading['integration_time'], FakeTCS34725.INTEGRATIONTIME_24MS)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
