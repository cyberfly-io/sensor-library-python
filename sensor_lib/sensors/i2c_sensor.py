from __future__ import annotations

from typing import Any, Dict, Optional

from sensor_lib.sensors.base_sensor import BaseSensor


class I2CSensor(BaseSensor):
    """Base class to share I2C setup between sensors."""

    DEFAULT_ADDRESS: Optional[int] = None

    def __init__(self, sensor_type: str, inputs: Optional[Dict[str, Any]] = None) -> None:
        self.address: Optional[int] = None
        self.i2c = None
        super().__init__(sensor_type, inputs)

    def optional_inputs(self):
        return ("address", "i2c_bus")

    def _setup(self) -> None:
        self.address = self.get_input("address", self.DEFAULT_ADDRESS)
        self.i2c = self.get_input("i2c_bus")
        if self.i2c is None:
            board = self.import_driver("board", error_hint="Ensure adafruit-blinka is installed")
            self.i2c = board.I2C()
        self._initialize_device()

    def _initialize_device(self) -> None:
        """Implemented by subclasses to create the sensor-specific driver."""

        raise NotImplementedError
