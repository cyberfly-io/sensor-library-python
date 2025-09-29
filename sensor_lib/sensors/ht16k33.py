from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class HT16K33(I2CSensor):
    """HT16K33 4-digit alphanumeric/7-segment display."""

    DEFAULT_ADDRESS = 0x70

    def __init__(self, inputs: Dict[str, Any]):
        self.display = None
        self._last_text = ""
        super().__init__('ht16k33', inputs)

    def optional_inputs(self):
        return (*super().optional_inputs(), 'text', 'align_right')

    def _initialize_device(self) -> None:
        segments_module = self.import_driver(
            'adafruit_ht16k33.segments',
            error_hint='pip install adafruit-circuitpython-ht16k33'
        )
        display_class = getattr(segments_module, 'Seg7x4')
        self.display = display_class(self.i2c, address=self.address or self.DEFAULT_ADDRESS)
        self.display.fill(0)

        initial = self.get_input('text')
        if initial:
            self.display_text(str(initial))

    def display_text(self, text: str, align_right: bool | None = None) -> None:
        sanitized = self._sanitize_text(text, align_right)
        self.display.print(sanitized)
        self._last_text = sanitized

    def clear(self) -> None:
        self.display.fill(0)
        self._last_text = ""

    def read(self) -> Dict[str, Any]:
        return {"text": self._last_text}

    def _sanitize_text(self, text: str, align_right: bool | None = None) -> str:
        align_flag = self.get_input('align_right', False) if align_right is None else align_right
        sanitized = str(text).strip()
        if len(sanitized) > 4:
            sanitized = sanitized[:4]
        if align_flag:
            return sanitized.rjust(4)
        return sanitized.ljust(4)
