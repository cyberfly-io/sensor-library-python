from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class TCS34725(I2CSensor):
    """TCS34725 RGB color sensor with IR filter and white LED."""

    DEFAULT_ADDRESS = 0x29

    def __init__(self, inputs: Dict[str, Any]):
        self.sensor = None
        super().__init__('tcs34725', inputs)

    def optional_inputs(self):
        return (*super().optional_inputs(), 'gain', 'integration_time')

    def _initialize_device(self) -> None:
        tcs_module = self.import_driver(
            'adafruit_tcs34725',
            error_hint='pip install adafruit-circuitpython-tcs34725'
        )
        self.sensor = tcs_module.TCS34725(
            self.i2c,
            address=self.address or self.DEFAULT_ADDRESS
        )

        gain = self.get_input('gain')
        if gain is not None:
            self.sensor.gain = self._coerce_gain(gain, tcs_module)

        integration_time = self.get_input('integration_time')
        if integration_time is not None:
            self.sensor.integration_time = self._coerce_integration_time(integration_time, tcs_module)

    def read(self) -> Dict[str, Any]:
        red, green, blue, clear = self.sensor.color_raw
        rgb_bytes = self.sensor.color_rgb_bytes
        lux = getattr(self.sensor, 'lux', None)
        color_temp = getattr(self.sensor, 'color_temperature', None)
        reading: Dict[str, Any] = {
            "raw": {
                "red": int(red),
                "green": int(green),
                "blue": int(blue),
                "clear": int(clear),
            },
            "rgb": {
                "r": int(rgb_bytes[0]),
                "g": int(rgb_bytes[1]),
                "b": int(rgb_bytes[2]),
            },
        }
        if lux is not None:
            reading['lux'] = float(lux)
        if color_temp is not None:
            reading['color_temperature'] = float(color_temp)
        reading['gain'] = getattr(self.sensor, 'gain', None)
        reading['integration_time'] = getattr(self.sensor, 'integration_time', None)
        return reading

    @staticmethod
    def _coerce_gain(value: Any, module) -> Any:
        if value is None:
            return value
        if isinstance(value, (int, float)):
            return value
        lookup_value = str(value).upper().replace(' ', '').replace('-', '_')
        if not lookup_value.startswith('GAIN_'):
            lookup_value = f'GAIN_{lookup_value}'
        if hasattr(module, lookup_value):
            return getattr(module, lookup_value)
        raise ValueError('gain must be a valid TCS34725 gain value (e.g., 1, 4, 16, 60 or "GAIN_4X")')

    @staticmethod
    def _coerce_integration_time(value: Any, module) -> Any:
        if value is None:
            return value
        if isinstance(value, (int, float)):
            return value
        lookup_value = str(value).upper().replace(' ', '').replace('-', '_')
        if not lookup_value.startswith('INTEGRATIONTIME'):
            lookup_value = f'INTEGRATIONTIME_{lookup_value}'
        if hasattr(module, lookup_value):
            return getattr(module, lookup_value)
        raise ValueError(
            'integration_time must be a numeric value in milliseconds or a valid constant like "INTEGRATIONTIME_24MS"'
        )
