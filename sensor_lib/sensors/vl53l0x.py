from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class VL53L0X(I2CSensor):
    DEFAULT_ADDRESS = 0x29

    def __init__(self, inputs: Dict[str, Any]):
        self.sensor = None
        super().__init__('vl53l0x', inputs)

    def optional_inputs(self):
        return (
            *super().optional_inputs(),
            'measurement_timing_budget',
            'signal_rate_limit',
        )

    def _initialize_device(self) -> None:
        adafruit_vl53l0x = self.import_driver(
            'adafruit_vl53l0x',
            error_hint='pip install adafruit-circuitpython-vl53l0x'
        )
        self.sensor = adafruit_vl53l0x.VL53L0X(
            self.i2c,
            address=self.address or self.DEFAULT_ADDRESS
        )

        timing_budget = self.get_input('measurement_timing_budget')
        if timing_budget is not None:
            try:
                self.sensor.measurement_timing_budget = int(timing_budget)
            except (AttributeError, ValueError, TypeError):
                raise ValueError('measurement_timing_budget must be an integer number of microseconds')

        signal_rate_limit = self.get_input('signal_rate_limit')
        if signal_rate_limit is not None:
            try:
                self.sensor.signal_rate_limit = float(signal_rate_limit)
            except (AttributeError, ValueError, TypeError):
                raise ValueError('signal_rate_limit must be a float value in MCPS')

    def read(self) -> Dict[str, Any]:
        distance_mm = int(self.sensor.range)
        return {
            "distance_mm": distance_mm,
            "distance_cm": distance_mm / 10.0,
        }
