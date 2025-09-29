from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class ADS1115(I2CSensor):
    DEFAULT_ADDRESS = 0x48
    VALID_CHANNELS = {0, 1, 2, 3}

    def __init__(self, inputs: Dict[str, Any]):
        self.ads = None
        self.analog_in = None
        self.channel_index = 0
        super().__init__('ads1115', inputs)

    def optional_inputs(self):
        return (
            *super().optional_inputs(),
            'channel',
            'gain',
            'data_rate',
        )

    def _initialize_device(self) -> None:
        ads_module = self.import_driver(
            'adafruit_ads1x15.ads1115',
            error_hint='pip install adafruit-circuitpython-ads1x15'
        )
        analog_module = self.import_driver(
            'adafruit_ads1x15.analog_in',
            error_hint='pip install adafruit-circuitpython-ads1x15'
        )

        self.ads = ads_module.ADS1115(
            self.i2c,
            address=self.address or self.DEFAULT_ADDRESS
        )

        gain = self.get_input('gain')
        if gain is not None:
            try:
                self.ads.gain = int(gain)
            except (AttributeError, TypeError, ValueError) as exc:
                raise ValueError('gain must be an integer supported by ADS1115 (e.g., 1, 2, 4, 8, 16)') from exc

        data_rate = self.get_input('data_rate')
        if data_rate is not None:
            try:
                self.ads.data_rate = int(data_rate)
            except (AttributeError, TypeError, ValueError) as exc:
                raise ValueError('data_rate must be an integer matching ADS1115 data rate setting') from exc

        channel = int(self.get_input('channel', 0))
        if channel not in self.VALID_CHANNELS:
            raise ValueError('channel must be an integer in range 0-3')
        self.channel_index = channel

        channel_pin = getattr(ads_module, f'P{channel}')
        self.analog_in = analog_module.AnalogIn(self.ads, channel_pin)

    def read(self) -> Dict[str, Any]:
        raw_value = int(self.analog_in.value)
        voltage_value = float(self.analog_in.voltage)
        return {
            "channel": self.channel_index,
            "raw": raw_value,
            "voltage": voltage_value,
            "gain": getattr(self.ads, 'gain', None),
        }
