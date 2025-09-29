from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.base_sensor import BaseSensor


class DS18B20(BaseSensor):
    """1-Wire DS18B20 temperature sensor."""

    UNIT_MAP = {
        "c": "celsius",
        "celsius": "celsius",
        "f": "fahrenheit",
        "fahrenheit": "fahrenheit",
        "k": "kelvin",
        "kelvin": "kelvin",
    }

    def __init__(self, inputs: Dict[str, Any]):
        self.sensor = None
        self.unit_key = "celsius"
        super().__init__('ds18b20', inputs)

    def optional_inputs(self):
        return ('sensor_id', 'unit')

    def _setup(self) -> None:
        w1therm = self.import_driver('w1thermsensor', error_hint='pip install w1thermsensor')
        sensor_id = self.get_input('sensor_id')
        unit = self.get_input('unit', 'celsius')
        self.unit_key = self.UNIT_MAP.get(str(unit).lower(), 'celsius')

        unit_enum = getattr(w1therm.W1ThermSensor, f"DEGREES_{self.unit_key[0].upper()}")
        sensor_type = w1therm.W1ThermSensor.THERM_SENSOR_DS18B20

        if sensor_id:
            self.sensor = w1therm.W1ThermSensor(sensor_type=sensor_type, sensor_id=sensor_id)
        else:
            self.sensor = w1therm.W1ThermSensor(sensor_type=sensor_type)

        self.unit_enum = unit_enum

    def read(self):
        temperature = float(self.sensor.get_temperature(self.unit_enum))
        return {
            "temperature": temperature,
            "unit": self.unit_key,
        }
