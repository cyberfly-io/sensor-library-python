from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.gpio_common import DigitalInputSensor


class DIN(DigitalInputSensor):
    def __init__(self, inputs: Dict[str, Any]):
        super().__init__('din', inputs)

    def read(self):
        return {"input": int(self.device.value)}
