from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class SHT31D(I2CSensor):
    """Sensirion SHT31-D temperature and humidity sensor."""

    DEFAULT_ADDRESS = 0x44

    def __init__(self, inputs: Dict[str, Any]):
        self.sensor = None
        super().__init__('sht31d', inputs)

    def optional_inputs(self):
        return (*super().optional_inputs(), 'heater')

    def _initialize_device(self) -> None:
        sht31d_module = self.import_driver(
            'adafruit_sht31d',
            error_hint='pip install adafruit-circuitpython-sht31d'
        )
        self.sensor = sht31d_module.SHT31D(
            self.i2c,
            address=self.address or self.DEFAULT_ADDRESS
        )

        heater = self.get_input('heater')
        if heater is not None and hasattr(self.sensor, 'heater'):
            self.sensor.heater = bool(heater)

    def read(self) -> Dict[str, Any]:
        return {
            "temperature": float(self.sensor.temperature),
            "humidity": float(self.sensor.relative_humidity),
            "heater": bool(getattr(self.sensor, 'heater', False)),
        }
