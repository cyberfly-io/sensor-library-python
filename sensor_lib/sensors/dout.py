from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.gpio_common import DigitalOutputSensor


class DOUT(DigitalOutputSensor):
    def __init__(self, inputs: Dict[str, Any]):
        super().__init__('dout', inputs)
