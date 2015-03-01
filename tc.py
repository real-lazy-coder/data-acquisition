#!/usr/bin/env python
import logging
from MAX31855 import MAX31855 as max
from random import randint
from functools import reduce
from datetime import datetime
from constants import *
from models import *

module_logger = logging.getLogger("application.Thermocouple")


class Thermocouple(object):
    """
    Thermocouple class to describe TC attributes
    """

    __thermocouple_temp_f = 0  # thermocouple temperature in fahrenheit
    __average_temp_f = 0  # average thermocouple temperature in fahrenheit
    __last_sample_time = datetime.now()  # last date/time a sample temperature was taken
    __last_log_time = datetime.now()  # last date/time a log was taken

    def __init__(self, p_tc_settings):
        self.tc_settings = p_tc_settings
        self.temperature_history = []

        # if we are working under the linux os initialize the MAX31855 TC
        if LINUX:
            try:
                self.__max31855 = max(p_cs_pin=self.tc_settings.cs, p_clock_pin=self.tc_settings.clk,
                                      p_data_pin=self.tc_settings.do, p_units="f")

                if DEBUG:
                    print 'cs: ' + str(self.__max31855.cs_pin)
                    print 'clock: ' + str(self.__max31855.clock_pin)
                    print 'data: ' + str(self.__max31855.data_pin)
                    print 'units: ' + str(self.__max31855.units)

                # log initialization to logger
                module_logger.info("Thermocouple Initialized: " + self.tc_settings.name)
            except Exception as e:
                module_logger.error(e)
                module_logger.info('Issues initializing the thermocouple')

        # if we are debugging update terminal
        if DEBUG:
            print "Thermocouple initialized: " + self.tc_settings.name

    @property
    def tc_temp(self):
        return self.__get_temp()

    @property
    def thermocouple_temp_f(self):
        return self.__thermocouple_temp_f

    @thermocouple_temp_f.setter
    def thermocouple_temp_f(self, value):
        self.__thermocouple_temp_f = float(value)

    @property
    def average_temp_f(self):
        return self.__get_average_temp()

    @property
    def last_sample_time(self):
        return self.__last_sample_time

    @last_sample_time.setter
    def last_sample_time(self, value):
        self.__last_sample_time = value

    @property
    def last_log_time(self):
        return self.__last_log_time

    @last_log_time.setter
    def last_log_time(self, value):
        self.__last_log_time = value

    def __get_temp(self):
        """Returns the current temperature.
        :rtype : float
        """

        if LINUX:
            try:
                if DEBUG:
                    module_logger.info('line before max31855.get()')
                tc_temp = self.__max31855.get()
            except Exception as e:
                module_logger.info('Error getting temp from MAX31855: ')
                module_logger.error(e)
                raise e

        if WINDOWS:
            tc_temp = float(randint(-30, 30))

        if DEBUG:
            print "Current Temp:\t", tc_temp

        return tc_temp

    def __get_average_temp(self):
        """Returns average temperature"""
        return reduce(lambda x, y: x + y, self.temperature_history) / len(self.temperature_history)

    def add_temp_history(self):
        """Get the current temperature and store it into temp history."""
        try:
            self.temperature_history.append(self.__get_temp())
        except Exception as e:
            module_logger.info("error appending to temperature_history.")
            module_logger.error(e)

    def store_temperature(self):
        """ Writes the average temperature """
        try:
            database.connect()  # connect to the database via peewee ORM

            # create an instance of the DataLog
            data_log = DataLog(tc=self.tc_settings, date_time=datetime.now(),
                               temperature=self.average_temp_f, uploaded=False)

            data_log.save()  # save data_log to table

            if DEBUG:
                print "Average Temp:\t", self.average_temp_f

            self.temperature_history = []  # clear the array

        except Exception as e:
            module_logger.info("Error writing to local database: ")
            module_logger.error(e)
            if DEBUG:
                print e
        finally:
            database.close()


if __name__ == '__main__':
    database.connect()
    t = []
    for tc in ThermocoupleSettings.select():
        t.append(Thermocouple(tc))
    database.close()

    for tc in t:
        tc.add_temp_history()
        tc.add_temp_history()
        tc.add_temp_history()
        tc.store_temperature()