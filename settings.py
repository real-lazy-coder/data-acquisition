#!/usr/bin/env python
import sqlite3 as lite
import time
import logging
from thermocouple import Thermocouple
from constants import *

module_logger = logging.getLogger("application.Settings")

# TODO: Add 2 modes: Edison & Non-Edison for running on a computer


class Settings(object):
    """ Describes attributes of the application """

    def __init__(self):
        """ class constructor """

        # Default property settings will be updated via the sqlite table
        self.__app_name = "Data_Acquisition_Logger"
        self.__event_loop_interval = 0.1

        self.__thermocouples = []

        # Update settings from database
        self.__get_database_settings()
        self.__get_thermocouples_from_db()

    @property
    def thermocouples(self):
        """
        :return: Thermocouples array
        """
        return self.__thermocouples

    @property
    def event_loop_interval(self):
        """
        Returns the sleep duration of the EventLoop() in application.py
        :return: float
        """
        return self.__event_loop_interval

    @event_loop_interval.setter
    def event_loop_interval(self, value):
        """
        :param value: float
        :return: None
        """
        self.__event_loop_interval = float(value)

    @property
    def app_name(self):
        """
        :return: String
        """
        """ Application Name """
        return self.__AppName

    @app_name.setter
    def app_name(self, value):
        """
        :param value: String
        :return: None
        """
        self.__AppName = value

    def __get_database_settings(self):
        """ get settings from database  """

        # app settings table definition
        # TODO: NOT IN USE - Update these settings anytime you update the table structure
        app_settings = ({
                            "tableName": "application_settings",
                            "columns": {
                                "id": 0,
                                "name": 1,
                                "description": 2,
                                "value": 3
                            }
                        })

        start = time.time()

        # connect to database
        db = lite.connect(APP_DB)

        # get app name from database
        c = db.execute("SELECT value FROM application_settings WHERE name = 'app_name'")
        self.app_name = str(c.fetchone()[0])

        # get event_loop_interval from database
        c = db.execute("SELECT value FROM application_settings WHERE name = 'event_loop_interval'")
        self.event_loop_interval = float(c.fetchone()[0])

        end = time.time()

        module_logger.info("App Name:\t\t\t\t" + self.app_name)

        if DEBUG:
            print "Event Loop Interval:\t" + str(self.event_loop_interval)
            print "Elapsed Time:\t\t\t" + str((end - start) * 1000.0)

    def __get_thermocouples_from_db(self):
        """
        Get all thermocouples from database and add to thermocouples property
        :return: None
        """

        # connect to database
        db = lite.connect(APP_DB)

        # get thermocouples from thermocouple_settings table
        c = db.execute("SELECT * FROM thermocouple_settings")

        # loop through c.results and add the thermocouple to self.__thermocouples
        for tc in c:
            temp = Thermocouple(tc[0], tc[1], tc[2], tc[3], tc[4], tc[5], tc[6], tc[7])
            self.__thermocouples.append(temp)

        if DEBUG:
            print "Thermocouples:\t" + str(self.__thermocouples.__len__())

        module_logger.info("Thermocouples: %s", self.__thermocouples.__len__())


if __name__ == "__main__":
    app = Settings()
