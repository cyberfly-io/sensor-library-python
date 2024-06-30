from gpiozero import OutputDevice

from sensor_lib.sensors import base_sensor
class DOUT(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('dout', inputs)
        self.pin_no = inputs.get('pin_no')
        self.device = OutputDevice(pin=self.pin_no, active_high=True)

    def read(self):
        return {"output": self.device.value}
