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

    def __init__(self, p_tc_settings=None):
        self.tc_settings = p_tc_settings
        self.temperature_history = []

        # if we are working under the linux os initialize the MAX31855 TC
        if LINUX:
            self.__max31855 = max(self.tc_settings.cs, self.tc_settings.clk, self.tc_settings.do, units="f")

        # log initialization to logger
        module_logger.info("Thermocouple Initialized")

        # if we are debugging update terminal
        if DEBUG:
            print "Thermocouple initialized."

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
        """Returns the current temperature."""

        if LINUX:
            tc_temp = self.__max31855.get()

        if WINDOWS:
            tc_temp = randint(-30, 30)

        if DEBUG:
            print "Current Temp:\t", tc_temp

        return tc_temp

    def __get_average_temp(self):
        """Returns average temperature"""
        return reduce(lambda x, y: x + y, self.temperature_history) / len(self.temperature_history)

    def add_temp_history(self):
        """Get the current temperature and store it into temp history."""
        self.temperature_history.append(self.__get_temp())

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
            module_logger.error("Error writing to local database: " + str(Exception.message))
            if DEBUG:
                print e
        finally:
            database.close()


if __name__ == '__main__':
    database.connect()
    tc = Thermocouple(ThermocoupleSettings.get())
    database.close()
    tc.add_temp_history()
    tc.add_temp_history()
    tc.add_temp_history()
    tc.store_temperature()