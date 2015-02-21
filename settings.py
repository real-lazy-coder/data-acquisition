#!/usr/bin/env python
import logging
from tc import Thermocouple
from models import *
from constants import *

module_logger = logging.getLogger(APP_NAME + ".Settings")


class AppSettings(object):
    """
    Describes attributes of the application
    """

    def __init__(self):
        self.__app_name = ''  # application name
        self.__event_loop_interval = 0.1  # time elapsed between event loop intervals

        self.__thermocouples = []  # array of thermocouples

        self.__get_settings()
        self.__get_thermocouples_from_db()

    @property
    def thermocouples(self):
        return self.__thermocouples

    @thermocouples.setter
    def thermocouples(self, value):
        self.__thermocouples = value

    @property
    def app_name(self):
        return self.__app_name

    @app_name.setter
    def app_name(self, value):
        self.__app_name = str(value)

    @property
    def event_loop_interval(self):
        return self.__event_loop_interval

    @event_loop_interval.setter
    def event_loop_interval(self, value):
        self.__event_loop_interval = float(value)

    def __get_settings(self):
        """
        Retrieve all settings from application.application_settings table and store them to class properties
        :return: None
        """

        database.connect()  # connect to the database via peewee ORM
        app_name_setting = Settings.select().where(Settings.name == 'app_name').get()
        self.app_name = app_name_setting.value  # assign app_name_setting.value to class property

        event_loop_setting = Settings.select().where(Settings.name == 'event_loop_interval').get()
        self.event_loop_interval = event_loop_setting.value  # assign event_loop_setting.value to class property

        database.close()  # close the database connection

    def __get_thermocouples_from_db(self):
        """
        Retrieve all thermocouples from the ThermocoupleSettings table and append it to the thermocouples class property
        :return: None
        """
        database.connect()  # connect to the database via peewee ORM

        # add all thermocouples to self.thermocouples array
        for tc in ThermocoupleSettings.select():
            t = Thermocouple(tc)
            self.thermocouples.append(t)

        database.close()

if __name__ == '__main__':
    AppSettings()