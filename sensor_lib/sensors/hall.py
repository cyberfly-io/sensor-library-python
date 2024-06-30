from gpiozero import DigitalInputDevice
from sensor_lib.sensors import base_sensor
class HALL(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('hall', inputs)
        self.pin_no = inputs.get('pin_no')

    def read(self):
        hall = DigitalInputDevice(self.pin_no, pull_up=True)
        return {"magnet": hall.value==0 } 
