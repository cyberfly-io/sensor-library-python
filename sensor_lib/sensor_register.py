from sensor_lib.sensors import dht11, vcgen, pir, din, hall
SENSOR_DICT = {
    'dht11':dht11.DHT11,
    'vcgen': vcgen.VCGEN,
    'pir':  pir.PIR,
    'din': din.DIN,
    'hall': hall.HALL
    # Add more sensors here, e.g., 'bmp180': BMP180,
}
