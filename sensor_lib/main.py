from sensor_lib.sensor_register import SENSOR_DICT
def create_sensor(sensor_type, inputs):
    if sensor_type in SENSOR_DICT:
        return SENSOR_DICT[sensor_type](inputs)
    else:
        raise ValueError(f"Sensor type {sensor_type} is not supported")