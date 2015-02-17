#!/usr/bin/env python
import logging
from wiringx86 import GPIOEdison as GPIO
from constants import *
from settings import Settings as AppSettings
from datetime import datetime, timedelta
from time import sleep


class Application():
    """
    Main application class
    """

    # Application settings
    data_logger = None

    # create logger for application
    logger = logging.getLogger(APP_NAME)

    def __init__(self):
        """ program setup and initialization. """

        # Initialize loggerConfig
        self.logger_config()

        # log loggerConfig results
        if DEBUG:
            print "Logger has been configured."
        self.logger.info("Logger has been configured")

        self.data_logger = AppSettings()

        # launch eventLoop
        self.event_loop()

    def logger_config(self):
        """configure logging settings"""

        # Set logging level to Debug
        self.logger.setLevel(logging.DEBUG)

        # create file handler which to log messages
        file_handler = logging.FileHandler(LOG_LOCATION + APP_NAME + ".log")

        # set file handler log level
        file_handler.setLevel(logging.DEBUG)

        # create console handler to log messages
        console_handler = logging.StreamHandler()

        # set console handler log level
        console_handler.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(log_formatter)
        console_handler.setFormatter(log_formatter)

        # add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def event_loop(self):
        """program loop for controller."""
        self.logger.info("eventLoop has started.")

        gpio = GPIO(debug=False)
        ledPin = 13
        ledState = gpio.HIGH
        gpio.pinMode(ledPin, gpio.OUTPUT)

        while True:

            try:
                for tc in self.data_logger.thermocouples:

                    sample_delta = (datetime.now() - tc.last_sample_time) > timedelta(seconds=tc.sample_interval)
                    log_delta = (datetime.now() - tc.last_log_time) > timedelta(seconds=tc.update_interval)

                    if sample_delta:
                        gpio.digitalWrite(ledPin, ledState)
                        ledState = gpio.LOW if ledState == gpio.HIGH else gpio.HIGH
                        tc.add_temp_history()
                        tc.last_sample_time = datetime.now()

                    if log_delta:
                        gpio.digitalWrite(ledPin, ledState)
                        ledState = gpio.LOW if ledState == gpio.HIGH else gpio.HIGH
                        tc.store_temperature()
                        tc.last_log_time = datetime.now()
            except:
                pass
            finally:
                # slow the event loop down to interval defined by Settings.py
                # this helps manage processor utilization
                sleep(self.data_logger.event_loop_interval)


if __name__ == "__main__":
    """ Main entry point to program """
    app = Application()