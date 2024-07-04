import board
import adafruit_mpu6050


from sensor_lib.sensors import base_sensor

class MPU6050(base_sensor.BaseSensor):
    def __init__(self, inputs):
        super().__init__('mpu6050', inputs)
        self.i2c = board.I2C()
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c, address=inputs.get('address', 0x68))



    def read(self):
        results = {"accelero":{"x":self.mpu.acceleration[0], "y":self.mpu.acceleration[1], "z":self.mpu.acceleration[2]}, 
                   "gyro":{"x":self.mpu.gyro[0], "y":self.mpu.gyro[1], "z":self.mpu.gyro[2]}, "temperature":self.mpu.temperature}
        return results
