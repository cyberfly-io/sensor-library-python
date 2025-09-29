from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class LCD1602(I2CSensor):
    """HD44780-compatible 16x2 character LCD driven over I2C backpack."""

    DEFAULT_ADDRESS = 0x27

    def __init__(self, inputs: Dict[str, Any]):
        self.lcd = None
        self._last_text = ""
        super().__init__('lcd1602', inputs)

    def optional_inputs(self):
        return (*super().optional_inputs(), 'columns', 'rows', 'text', 'auto_linebreaks')

    def _initialize_device(self) -> None:
        lcd_module = self.import_driver(
            'adafruit_character_lcd.character_lcd_i2c',
            error_hint='pip install adafruit-circuitpython-charlcd'
        )
        columns = int(self.get_input('columns', 16))
        rows = int(self.get_input('rows', 2))
        auto_linebreaks = bool(self.get_input('auto_linebreaks', True))

        init_kwargs: Dict[str, Any] = {}
        if self.address is not None:
            init_kwargs['address'] = self.address

        self.lcd = lcd_module.Character_LCD_I2C(self.i2c, columns, rows, **init_kwargs)
        self.lcd.auto_linebreaks = auto_linebreaks
        if hasattr(self.lcd, 'backlight'):
            self.lcd.backlight = True
        self.clear()

        initial_text = self.get_input('text')
        if initial_text:
            self.display_text(str(initial_text))

    def display_text(self, text: str, clear: bool = True) -> None:
        """Display the provided text on the LCD."""

        sanitized = self._sanitize_text(text)
        if clear:
            self.clear()
        self.lcd.message = sanitized
        self._last_text = sanitized

    def append_text(self, text: str) -> None:
        """Append text to the current message without clearing."""

        sanitized = self._sanitize_text(text)
        self.lcd.message = (self._last_text + sanitized)
        self._last_text += sanitized

    def clear(self) -> None:
        if hasattr(self.lcd, 'clear'):
            self.lcd.clear()
        self._last_text = ""

    def read(self) -> Dict[str, Any]:
        return {"text": self._last_text}

    @staticmethod
    def _sanitize_text(text: str) -> str:
        return str(text)
