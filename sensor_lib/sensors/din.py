from gpiozero import DigitalInputDevice
from sensor_lib.sensors import base_sensor
class DIN(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('din', inputs)
        self.pin_no = inputs.get('pin_no')

    def read(self):
        did = DigitalInputDevice(self.pin_no)
        return did.value  
