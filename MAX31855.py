#!/usr/bin/env python
from constants import *
from wiringx86 import GPIOEdison as GPIO


class MAX31855(object):
    """Python driver for [MAX38155 Cold-Junction Compensated Thermocouple-to-Digital Converter](http://www.maximintegrated.com/datasheet/index.mvp/id/7273)
     Requires:
     - The [GPIO Library](https://code.google.com/p/raspberry-gpio-python/) (Already on most Raspberry Pi OS builds)
     - A [Raspberry Pi](http://www.raspberrypi.org/)
    """

    def __init__(self, cs_pin, clock_pin, data_pin, units="f"):
        """
        Initialize Soft (Bitbang) SPI Bus
        :param cs_pin: Chip Select (CS) | Slave Select (SS) pin (Any GPIO)
        :param clock_pin: Clock (SCLK / SCK / CLK) pin (Any GPIO)
        :param data_pin: Data input (SO / MOSI / DO) pin (Any GPIO)
        :param units: (optional) unit of measurement to return.  ("f" (default) | "c" | "k")
        :return: None
        """

        self.__gpio = GPIO(debug=False)
        self.cs_pin = cs_pin
        self.clock_pin = clock_pin
        self.data_pin = data_pin
        self.units = units
        self.data = None

        # Initialize needed GPIO
        if DEBUG:
            print self.__gpio.OUTPUT

        self.__gpio.pinMode(self.cs_pin, self.__gpio.OUTPUT)
        self.__gpio.pinMode(self.clock_pin, self.__gpio.OUTPUT)
        self.__gpio.pinMode(self.data_pin, self.__gpio.INPUT)

        # Pull chip select high to make chip inactive
        self.__gpio.digitalWrite(self.cs_pin, self.__gpio.HIGH)

    def get(self):
        """Reads SPI bus and returns current value of thermocouple."""
        self.read()
        self.check_errors()
        return getattr(self, "to_" + self.units)(self.data_to_tc_temperature())

    def get_rj(self):
        """Reads SPI bus and returns current value of reference junction."""
        self.read()
        return getattr(self, "to_" + self.units)(self.data_to_rj_temperature())

    def read(self):
        """Reads 32 bits of the SPI bus & stores as an integer in self.data."""
        bytes_to = 0
        # Select the chip
        self.__gpio.digitalWrite(self.cs_pin, self.__gpio.LOW)
        # Read in 32 bits
        for i in range(32):
            self.__gpio.digitalWrite(self.clock_pin, self.__gpio.LOW)
            bytes_to <<= 1
            if self.__gpio.digitalRead(self.data_pin):
                bytes_to |= 1
            self.__gpio.digitalWrite(self.clock_pin, self.__gpio.HIGH)
        # Deselect the chip
        self.__gpio.digitalWrite(self.cs_pin, self.__gpio.HIGH)
        # Save data
        self.data = bytes_to

    def check_errors(self, data_32=None):
        """Checks error bits to see if there are any SCV, SCG, or OC faults"""
        if data_32 is None:
            data_32 = self.data
        any_errors = (data_32 & 0x10000) != 0  # Fault bit, D16
        no_connection = (data_32 & 1) != 0  # OC bit, D0
        short_to_ground = (data_32 & 2) != 0  # SCG bit, D1
        short_to_vcc = (data_32 & 4) != 0  # SCV bit, D2
        if any_errors:
            if no_connection:
                raise MAX31855Error("No Connection")
            elif short_to_ground:
                raise MAX31855Error("Thermocouple short to ground")
            elif short_to_vcc:
                raise MAX31855Error("Thermocouple short to VCC")
            else:
                # Perhaps another SPI device is trying to send data?
                # Did you remember to initialize all other SPI devices?
                raise MAX31855Error("Unknown Error")

    def data_to_tc_temperature(self, data_32=None):
        """Takes an integer and returns a thermocouple temperature in celsius."""
        if data_32 is None:
            data_32 = self.data
        tc_data = ((data_32 >> 18) & 0x3FFF)
        return self.convert_tc_data(tc_data)

    def data_to_rj_temperature(self, data_32=None):
        """Takes an integer and returns a reference junction temperature in celsius."""
        if data_32 is None:
            data_32 = self.data
        rj_data = ((data_32 >> 4) & 0xFFF)
        return self.convert_rj_data(rj_data)

    @staticmethod
    def convert_tc_data(tc_data):
        """Convert thermocouple data to a useful number (celsius)."""
        if tc_data & 0x2000:
            # two's compliment
            without_resolution = ~tc_data & 0x1FFF
            without_resolution += 1
            without_resolution *= -1
        else:
            without_resolution = tc_data & 0x1FFF
        return without_resolution * 0.25

    @staticmethod
    def convert_rj_data(rj_data):
        """Convert reference junction data to a useful number (celsius)."""
        if rj_data & 0x800:
            without_resolution = ~rj_data & 0x7FF
            without_resolution += 1
            without_resolution *= -1
        else:
            without_resolution = rj_data & 0x7FF
        return without_resolution * 0.0625

    @staticmethod
    def to_c(celsius):
        """Celsius passthrough for generic to_* method."""
        return celsius

    @staticmethod
    def to_k(celsius):
        """Convert celsius to kelvin."""
        return celsius + 273.15

    @staticmethod
    def to_f(celsius):
        """Convert celsius to fahrenheit."""
        return celsius * 9.0 / 5.0 + 32

    def cleanup(self):
        """Selective GPIO cleanup"""
        self.__gpio.pinMode(self.cs_pin, self.__gpio.IN)
        self.__gpio.pinMode(self.clock_pin, self.__gpio.IN)


class MAX31855Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == "__main__":

    # Multi-chip example
    import time

    cs_pins = [4]
    clock_pin = 5
    data_pin = 3
    units = "f"
    thermocouples = []
    for cs_pin in cs_pins:
        thermocouples.append(MAX31855(cs_pin, clock_pin, data_pin, units))
    running = True
    while running:
        try:
            for thermocouple in thermocouples:
                rj = thermocouple.get_rj()
                try:
                    tc = thermocouple.get()
                except MAX31855Error as e:
                    tc = "Error: " + e.value
                    running = False
                print("tc: {} and rj: {}".format(tc, rj))
            time.sleep(1)
        except KeyboardInterrupt:
            running = False
    for thermocouple in thermocouples:
        thermocouple.cleanup()

