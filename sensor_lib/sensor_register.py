from sensor_lib.sensors import dht11, vcgen, pir, din, hall, water, dout
SENSOR_DICT = {
    'dht11':dht11.DHT11,
    'vcgen': vcgen.VCGEN,
    'pir':  pir.PIR,
    'din': din.DIN,
    'hall': hall.HALL,
    'water': water.WATER,
    'dout': dout.DOUT,
    # Add more sensors here, e.g., 'bmp180': BMP180,
}
