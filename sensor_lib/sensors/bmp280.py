from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class BMP280(I2CSensor):
    DEFAULT_ADDRESS = 0x77

    def __init__(self, inputs: Dict[str, Any]):
        self.bmp280 = None
        super().__init__('bmp280', inputs)

    def _initialize_device(self) -> None:
        adafruit_bmp280 = self.import_driver('adafruit_bmp280', error_hint='pip install adafruit-circuitpython-bmp280')
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c, address=self.address or self.DEFAULT_ADDRESS)
        self.bmp280.sea_level_pressure = self.get_input('sea_level_pressure', 1013.25)

    def read(self):
        return {
            "altitude": float(self.bmp280.altitude),
            "temperature": float(self.bmp280.temperature),
            "pressure": float(self.bmp280.pressure),
        }
