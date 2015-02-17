#!/usr/bin/env python
import logging
import sqlite3
from MAX31855 import MAX31855 as max
from random import randint
from functools import reduce
from datetime import datetime
from constants import *

module_logger = logging.getLogger("application.Thermocouple")


class Thermocouple:
    """
    Thermocouple class to describe TC attributes

    """

    # table structure
    __id = 0
    __name = ""
    __description = ""
    __do = 0
    __cs = 0
    __clk = 0
    __update_interval = 0.0
    __sample_interval = 0.0
    # end table structure

    # thermocouple temperature in fahrenheit
    __thermocouple_temp_f = 0

    # average thermocouple temperature in fahrenheit
    __average_temp_f = 0

    # last date/time a sample temperature was taken
    __last_sample_time = datetime.now()

    # last date/time a log was taken
    __last_log_time = datetime.now()

    def __init__(self, p_id=0, p_name="empty", p_desc="empty", p_do=0, p_cs=0, p_clk=0, p_update_interval=0,
                 p_sample_interval=0):
        self.__id = p_id
        self.__name = p_name
        self.__description = p_desc
        self.__do = p_do
        self.__cs = p_cs
        self.__clk = p_clk
        self.__update_interval = p_update_interval
        self.__sample_interval = p_sample_interval
        self.temperature_history = []

        # if we are working under the linux os initialize the MAX31855
        if LINUX:
            self.__max31855 = max(self.__cs, self.__clk, self.__do, units="f")

        # if we are working under the windows os, we are debugging.  Show dummy data.
        if WINDOWS:
            # TODO: Add windows dummy data
            pass

        # log initialization to logger
        module_logger.info("Thermocouple Initialized")

        # if we are debugging update terminal
        if DEBUG:
            print "Thermocouple initialized."

    @property
    def sample_interval(self):
        return self.__sample_interval

    @property
    def update_interval(self):
        return self.__update_interval

    @property
    def last_log_time(self):
        return self.__last_log_time

    @last_log_time.setter
    def last_log_time(self, value):
        self.__last_log_time = value

    @property
    def last_sample_time(self):
        return self.__last_sample_time

    @last_sample_time.setter
    def last_sample_time(self, value):
        self.__last_sample_time = value

    @property
    def thermocouple_temp_f(self):
        """
        Thermocouple Temperature F
        :return: float
        """
        return self.__thermocouple_temp_f

    @thermocouple_temp_f.setter
    def thermocouple_temp_f(self, value):
        """
        Set Thermocouple Temperature F
        :param value:
        :return: float
        """
        self.__thermocouple_temp_f = value

    @property
    def average_temp_f(self):
        """
        Average Temperature F
        :return: float
        """
        return self.__get_average_temp()

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
        temp = self.__get_temp()
        self.temperature_history.append(temp)

    def store_temperature(self):
        """ Writes the average temperature """
        try:
            data = (self.__id, datetime.now(), self.average_temp_f, 0)

            if DEBUG:
                print "Average Temp:\t", self.average_temp_f

            # connect to database
            db = sqlite3.connect(APP_DB)

            # execute sql statement
            c = db.execute("INSERT INTO data_log VALUES (?, ?, ?, ?)", data)

            # commit to database
            db.commit()

            # clear the array
            self.temperature_history = []
        except Exception:
            module_logger.error("Error writing to local database: " + Exception.message)
        finally:
            pass


if __name__ == "__main__":
    tc = Thermocouple()
    tc.add_temp_history()
    tc.add_temp_history()
    tc.add_temp_history()
    tc.store_temperature()
