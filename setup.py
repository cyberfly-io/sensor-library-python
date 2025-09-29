from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent
README_PATH = BASE_DIR / "README.md"

setup(
    name="sensor-library-python",
    version="0.2.0",
    description="Unified Raspberry Pi sensor wrapper with I2C/1-Wire/display helpers",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Cyberfly.io",
    url="https://github.com/cyberfly-io/sensor-library-python",
    license="MIT",
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "Adafruit_DHT",
        "RaspberryPiVcgencmd",
        "gpiozero",
        "adafruit-circuitpython-bmp280",
        "adafruit-circuitpython-mpu6050",
        "adafruit-circuitpython-bme280",
        "adafruit-circuitpython-bh1750",
        "adafruit-blinka",
        "w1thermsensor",
        "adafruit-circuitpython-bme680",
        "adafruit-circuitpython-ccs811",
        "adafruit-circuitpython-vl53l0x",
        "adafruit-circuitpython-ads1x15",
        "adafruit-circuitpython-charlcd",
        "adafruit-circuitpython-ht16k33",
        "adafruit-circuitpython-sht31d",
        "adafruit-circuitpython-tcs34725",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ],
    keywords="raspberrypi sensors i2c spi gpio",
)
