from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class BME680(I2CSensor):
    DEFAULT_ADDRESS = 0x77

    def __init__(self, inputs: Dict[str, Any]):
        self.sensor = None
        super().__init__('bme680', inputs)

    def _initialize_device(self) -> None:
        adafruit_bme680 = self.import_driver(
            'adafruit_bme680',
            error_hint='pip install adafruit-circuitpython-bme680'
        )
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(
            self.i2c,
            address=self.address or self.DEFAULT_ADDRESS
        )
        sea_level_pressure = self.get_input('sea_level_pressure', 1013.25)
        self.sensor.sea_level_pressure = sea_level_pressure

    def read(self):
        return {
            "temperature": float(self.sensor.temperature),
            "humidity": float(self.sensor.humidity),
            "pressure": float(self.sensor.pressure),
            "gas": float(self.sensor.gas),
        }
