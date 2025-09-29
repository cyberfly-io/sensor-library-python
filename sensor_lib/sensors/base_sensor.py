from __future__ import annotations

import abc
import importlib
from typing import Any, Dict, Iterable, Optional


class BaseSensor(abc.ABC):
    """Common functionality shared by every sensor implementation."""

    def __init__(self, sensor_type: str, inputs: Optional[Dict[str, Any]] = None) -> None:
        self.sensor_type = sensor_type
        self.inputs: Dict[str, Any] = inputs.copy() if inputs else {}
        self._validate_inputs()
        self._setup()

    # ---------------------------------------------------------------------
    # Hooks for subclasses
    # ---------------------------------------------------------------------
    def required_inputs(self) -> Iterable[str]:
        """List input keys that must be provided for the sensor to work."""

        return ()

    def optional_inputs(self) -> Iterable[str]:
        """List optional inputs for documentation/validation purposes."""

        return ()

    def _setup(self) -> None:
        """Prepare hardware resources. Subclasses can override when needed."""

    @abc.abstractmethod
    def read(self) -> Dict[str, Any]:
        """Read a snapshot from the sensor and return structured data."""

    # ------------------------------------------------------------------
    # Helpers shared by subclasses
    # ------------------------------------------------------------------
    def get_input(self, key: str, default: Any = None) -> Any:
        return self.inputs.get(key, default)

    def _validate_inputs(self) -> None:
        missing = [key for key in self.required_inputs() if self.inputs.get(key) is None]
        if missing:
            required = ", ".join(sorted(set(self.required_inputs())))
            raise ValueError(
                f"Missing required inputs for {self.sensor_type}: {', '.join(missing)}. "
                f"Required inputs: {required}"
            )

    @staticmethod
    def import_driver(module_name: str, error_hint: Optional[str] = None):
        """Import a hardware driver module with a helpful error message."""

        try:
            return importlib.import_module(module_name)
        except ImportError as exc:  # pragma: no cover - exercised indirectly
            hint = f" ({error_hint})" if error_hint else ""
            raise RuntimeError(
                f"Unable to import {module_name}{hint}. Ensure the dependency is installed and "
                "your hardware is configured correctly."
            ) from exc