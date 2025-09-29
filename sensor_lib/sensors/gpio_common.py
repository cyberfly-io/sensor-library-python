from __future__ import annotations

from typing import Any, Dict, Optional

from sensor_lib.sensors.base_sensor import BaseSensor


class DigitalInputSensor(BaseSensor):
    """Base class for single-pin digital input sensors."""

    pull_up: bool = False

    def __init__(self, sensor_type: str, inputs: Optional[Dict[str, Any]] = None) -> None:
        self.device = None
        super().__init__(sensor_type, inputs)

    def required_inputs(self):
        return ("pin_no",)

    def _setup(self) -> None:
        gpiozero = self.import_driver("gpiozero", error_hint="pip install gpiozero")
        DigitalInputDevice = getattr(gpiozero, "DigitalInputDevice")
        pin_no = self.get_input("pin_no")
        if pin_no is None:
            raise ValueError("pin_no must be provided for digital input sensors")
        self.device = DigitalInputDevice(pin_no, pull_up=self.pull_up)

    def read(self):
        return {"value": int(self.device.value) if self.device else 0}


class DigitalOutputSensor(BaseSensor):
    """Base class for single-pin digital output sensors."""

    def __init__(self, sensor_type: str, inputs: Optional[Dict[str, Any]] = None) -> None:
        self.device = None
        super().__init__(sensor_type, inputs)

    def required_inputs(self):
        return ("pin_no",)

    def _setup(self) -> None:
        gpiozero = self.import_driver("gpiozero", error_hint="pip install gpiozero")
        OutputDevice = getattr(gpiozero, "OutputDevice")
        pin_no = self.get_input("pin_no")
        active_high = bool(self.get_input("active_high", True))
        initial_value = bool(self.get_input("initial_value", False))
        if pin_no is None:
            raise ValueError("pin_no must be provided for digital output sensors")
        self.device = OutputDevice(pin=pin_no, active_high=active_high, initial_value=initial_value)

    def read(self):
        return {"output": bool(self.device.value) if self.device else False}
