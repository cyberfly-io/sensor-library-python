from RaspberryPiVcgencmd import Vcgencmd
from sensor_lib.sensors import base_sensor
class VCGEN(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('vcgen', inputs={})

    def read(self):
        cpu_temp = Vcgencmd().get_cpu_temp()
        results = {"cpu_temperature":cpu_temp}
        return results
