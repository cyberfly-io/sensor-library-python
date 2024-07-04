import board
import adafruit_bmp280

from sensor_lib.sensors import base_sensor

class BMP280(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('bmp280', inputs)
        self.i2c = board.I2C()
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c, address=inputs.get('address', 0x77))
        self.bmp280.sea_level_pressure = 1013.25


    def read(self):
        results = {"altitude":self.bmp280.altitude, "temperature":self.bmp280.temperature, "pressure":self.bmp280.pressure}
        return results
