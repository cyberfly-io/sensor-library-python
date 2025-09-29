from __future__ import annotations

import time
from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class CCS811(I2CSensor):
    DEFAULT_ADDRESS = 0x5A
    DATA_READY_RETRIES = 10
    DATA_READY_DELAY_SEC = 0.05

    def __init__(self, inputs: Dict[str, Any]):
        self.sensor = None
        self.temperature_offset = 0.0
        self.baseline = None
        super().__init__('ccs811', inputs)

    def optional_inputs(self):
        return (*super().optional_inputs(), 'temperature_offset', 'baseline')

    def _initialize_device(self) -> None:
        adafruit_ccs811 = self.import_driver(
            'adafruit_ccs811',
            error_hint='pip install adafruit-circuitpython-ccs811'
        )
        self.sensor = adafruit_ccs811.CCS811(
            self.i2c,
            address=self.address or self.DEFAULT_ADDRESS
        )

        self.temperature_offset = float(self.get_input('temperature_offset', 0.0))
        if self.temperature_offset:
            try:
                self.sensor.temperature_offset = self.temperature_offset
            except AttributeError:
                pass

        baseline = self.get_input('baseline')
        if baseline is not None:
            try:
                self.sensor.baseline = int(baseline)
            except (AttributeError, ValueError):
                raise ValueError('baseline must be an integer between 0 and 65535')
        self.baseline = baseline

    def _wait_for_data(self) -> None:
        if not hasattr(self.sensor, 'data_ready'):
            return
        for _ in range(self.DATA_READY_RETRIES):
            if self.sensor.data_ready:
                return
            time.sleep(self.DATA_READY_DELAY_SEC)
        raise RuntimeError('CCS811 data not ready yet')

    def read(self):
        self._wait_for_data()
        reading = {
            "eco2": float(self.sensor.eco2),
            "tvoc": float(self.sensor.tvoc),
            "temperature": float(self.sensor.temperature),
        }
        if hasattr(self.sensor, 'baseline'):
            baseline = getattr(self.sensor, 'baseline')
            if baseline is not None:
                reading['baseline'] = int(baseline)
        return reading
