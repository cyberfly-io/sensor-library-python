from __future__ import annotations

from typing import Any, Dict, Optional

from sensor_lib.sensors.passive_sensor import PassiveSensor


class PIR(PassiveSensor):
    def __init__(self, inputs: Dict[str, Any]):
        self.pin_no: Optional[int] = None
        self.pir = None
        super().__init__('pir', inputs)

    def required_inputs(self):
        return ('pin_no',)

    def _setup(self) -> None:
        gpiozero = self.import_driver('gpiozero', error_hint='pip install gpiozero')
        MotionSensor = getattr(gpiozero, 'MotionSensor')
        self.pin_no = self.get_input('pin_no')
        self.pir = MotionSensor(self.pin_no)

    def read(self):
        return {
            "motion": bool(self.pir.motion_detected),
            "value": int(self.pir.value),
        }

