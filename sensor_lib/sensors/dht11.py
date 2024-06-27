import Adafruit_DHT
from sensor_lib.sensors import base_sensor
class DHT11(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('dht11', inputs)
        self.sensor = Adafruit_DHT.DHT11
        self.pin_no = inputs.get('pin_no')

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin_no)
        results = {"humidity":humidity, "temperature":temperature}
        return results