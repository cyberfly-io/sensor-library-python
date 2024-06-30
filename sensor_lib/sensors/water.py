from gpiozero import DigitalInputDevice
from sensor_lib.sensors import base_sensor
class WATER(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('water', inputs)
        self.pin_no = inputs.get('pin_no')

    def read(self):
        hall = DigitalInputDevice(self.pin_no)
        return {"water": hall.value==0 } 
