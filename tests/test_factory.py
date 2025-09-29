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


class FakeMPU6050:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address
        self.acceleration = (1.0, 2.0, 3.0)
        self.gyro = (0.1, 0.2, 0.3)
        self.temperature = 24.5


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

        bh_module = types.ModuleType('adafruit_bh1750')
        bh_module.AmbientLightSensor = FakeBH1750
        add_module('adafruit_bh1750', bh_module)

        mpu_module = types.ModuleType('adafruit_mpu6050')
        mpu_module.MPU6050 = FakeMPU6050
        add_module('adafruit_mpu6050', mpu_module)

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


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
