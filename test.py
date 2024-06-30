from sensor_lib.main import create_sensor

sensor = create_sensor('pir', {"pin_no":4})

def motion():
   print("motion detected")


sensor.pir.when_motion = motion
while 1:
    pass
