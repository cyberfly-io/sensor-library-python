from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.gpio_common import DigitalInputSensor


class WATER(DigitalInputSensor):
    def __init__(self, inputs: Dict[str, Any]):
        super().__init__('water', inputs)

    def read(self):
        return {"water": bool(self.device.value == 0)}
