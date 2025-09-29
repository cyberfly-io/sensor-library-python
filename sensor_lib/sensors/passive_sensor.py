from __future__ import annotations

from typing import Any, Dict, Optional

from sensor_lib.sensors.base_sensor import BaseSensor


class PassiveSensor(BaseSensor):
    """Base class for sensors that expose state via GPIO callbacks."""

    def __init__(self, sensor_type: str, inputs: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(sensor_type, inputs)

    def read(self) -> Dict[str, Any]:  # pragma: no cover - subclasses should override
        raise NotImplementedError("Passive sensors must implement the read method")
