from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.gpio_common import DigitalInputSensor


class HALL(DigitalInputSensor):
    pull_up = True

    def __init__(self, inputs: Dict[str, Any]):
        super().__init__('hall', inputs)

    def read(self):
        return {"magnet": bool(self.device.value == 0)}
