from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.base_sensor import BaseSensor


class VCGEN(BaseSensor):
    def __init__(self, inputs):
        self.vcgencmd = None
        super().__init__('vcgen', inputs or {})

    def _setup(self) -> None:
        Vcgencmd = self.import_driver('RaspberryPiVcgencmd', error_hint='pip install RaspberryPiVcgencmd')
        self.vcgencmd = Vcgencmd.Vcgencmd()

    def read(self):
        cpu_temp = self.vcgencmd.get_cpu_temp()
        return {"cpu_temperature": cpu_temp}
