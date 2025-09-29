from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class BH1750(I2CSensor):
    DEFAULT_ADDRESS = 0x23

    def __init__(self, inputs: Dict[str, Any]):
        self.sensor = None
        super().__init__('bh1750', inputs)

    def _initialize_device(self) -> None:
        adafruit_bh1750 = self.import_driver('adafruit_bh1750', error_hint='pip install adafruit-circuitpython-bh1750')
        self.sensor = adafruit_bh1750.AmbientLightSensor(self.i2c, address=self.address or self.DEFAULT_ADDRESS)

    def read(self):
        return {"illuminance": float(self.sensor.lux)}
