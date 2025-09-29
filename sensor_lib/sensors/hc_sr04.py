from __future__ import annotations

from typing import Any, Dict, Optional

from sensor_lib.sensors.base_sensor import BaseSensor


class HCSR04(BaseSensor):
    """Ultrasonic distance sensor using gpiozero.DistanceSensor."""

    def __init__(self, inputs: Dict[str, Any]):
        self.trigger_pin: Optional[int] = None
        self.echo_pin: Optional[int] = None
        self.sensor = None
        super().__init__('hc_sr04', inputs)

    def required_inputs(self):
        return ('trigger_pin', 'echo_pin')

    def optional_inputs(self):
        return ('max_distance', 'threshold_distance')

    def _setup(self) -> None:
        gpiozero = self.import_driver('gpiozero', error_hint='pip install gpiozero')
        DistanceSensor = getattr(gpiozero, 'DistanceSensor')
        self.trigger_pin = self.get_input('trigger_pin')
        self.echo_pin = self.get_input('echo_pin')
        max_distance = self.get_input('max_distance', 1.0)
        threshold_distance = self.get_input('threshold_distance', 0.3)
        self.sensor = DistanceSensor(
            echo=self.echo_pin,
            trigger=self.trigger_pin,
            max_distance=max_distance,
            threshold_distance=threshold_distance,
        )

    def read(self):
        return {
            "distance_m": float(self.sensor.distance),
            "is_within_threshold": bool(self.sensor.distance <= self.sensor.threshold_distance),
        }
