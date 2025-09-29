from __future__ import annotations

from typing import Any, Dict, Optional

from sensor_lib.sensors.base_sensor import BaseSensor


class DHT11(BaseSensor):
    def __init__(self, inputs: Dict[str, Any]):
        self.driver = None
        self.pin_no: Optional[int] = None
        super().__init__('dht11', inputs)

    def required_inputs(self):
        return ('pin_no',)

    def _setup(self) -> None:
        self.driver = self.import_driver('Adafruit_DHT', error_hint='pip install Adafruit_DHT')
        self.pin_no = self.get_input('pin_no')
        if self.pin_no is None:
            raise ValueError('pin_no is required for DHT11 sensor')
        self.sensor = getattr(self.driver, 'DHT11')

    def read(self):
        humidity, temperature = self.driver.read_retry(self.sensor, self.pin_no)
        return {"humidity": humidity, "temperature": temperature}