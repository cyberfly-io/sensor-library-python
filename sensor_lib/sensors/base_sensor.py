class BaseSensor:
    def __init__(self, sensor_type, inputs):
        self.sensor_type = sensor_type
        self.inputs = inputs

    def read(self):
        raise NotImplementedError("This method should be overridden by subclasses")