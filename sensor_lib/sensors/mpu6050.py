from __future__ import annotations

from typing import Any, Dict

from sensor_lib.sensors.i2c_sensor import I2CSensor


class MPU6050(I2CSensor):
    DEFAULT_ADDRESS = 0x68

    def __init__(self, inputs: Dict[str, Any]):
        self.mpu = None
        super().__init__('mpu6050', inputs)

    def _initialize_device(self) -> None:
        adafruit_mpu6050 = self.import_driver('adafruit_mpu6050', error_hint='pip install adafruit-circuitpython-mpu6050')
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c, address=self.address or self.DEFAULT_ADDRESS)

    def read(self):
        acceleration = self.mpu.acceleration
        gyro = self.mpu.gyro
        return {
            "acceleration": {"x": acceleration[0], "y": acceleration[1], "z": acceleration[2]},
            "gyro": {"x": gyro[0], "y": gyro[1], "z": gyro[2]},
            "temperature": float(self.mpu.temperature),
        }
