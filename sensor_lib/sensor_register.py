from sensor_lib.sensors import dht11, vcgen, pir, din, hall, water, dout, bmp280
SENSOR_DICT = {
    'dht11':dht11.DHT11,
    'vcgen': vcgen.VCGEN,
    'pir':  pir.PIR,
    'din': din.DIN,
    'hall': hall.HALL,
    'water': water.WATER,
    'dout': dout.DOUT,
    'bmp280': bmp280.BMP280
    # Add more sensors here, e.g., 'bmp180': BMP180,
}
