from sensor_lib.sensors import passive_sensor
from gpiozero import MotionSensor

class PIR(passive_sensor.PassiveSensor):
    def __init__(self, inputs):
        super().__init__('pir', inputs)
        self.pin_no = inputs.get('pin_no')
        self.pir = MotionSensor(self.pin_no)

