#!/usr/bin/env python
import logging
from datetime import datetime, timedelta
from time import sleep

from constants import *
from settings import AppSettings


if LINUX:
    import pyupm_i2clcd as lcd


class Application():
    """
    Main application class
    """

    # create logger for application
    logger = logging.getLogger(APP_NAME)

    # rgb lcd display
    lcdDisplay = None

    def __init__(self):
        """ program setup and initialization. """

        # if linux setup lcd
        if LINUX:
            self.lcd_setup()

        # Initialize loggerConfig
        self.logger_config()

        # log loggerConfig results
        if DEBUG:
            print "Logger has been configured."
        self.logger.info("Logger has been configured")

        self.logger.info("PLATFORM: " + str(PLATFORM))
        self.logger.info("WINDOWS: " + str(WINDOWS))
        self.logger.info("LINUX: " + str(LINUX))
        self.logger.info("DEBUG: " + str(DEBUG))
        self.logger.info("LOG_LOCATION: " + str(LOG_LOCATION))
        self.logger.info("APP_DB: " + str(APP_DB))

        if DEBUG:
            print "PLATFORM: " + str(PLATFORM)
            print "WINDOWS: " + str(WINDOWS)
            print "LINUX: " + str(LINUX)
            print "DEBUG: " + str(DEBUG)
            print "LOG_LOCATION: " + str(LOG_LOCATION)
            print "APP_DB: " + str(APP_DB)

        self.data_logger = AppSettings()

        # launch eventLoop
        self.event_loop()

    def lcd_setup(self):
        """
        setup pyupm_i2clcd RGB LCD
        # bus	i2c bus to use
        # address	the slave address the lcd is registered on
        # address	the slave address the rgb backlight is on
        Jhd1313m1	(
            int 	bus,
            int 	lcdAddress = 0x3E,
            int 	rgbAddress = 0x62
        )
        :return: None
        """
        self.lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)

        # set lcd cursor to (0,0)
        self.lcdDisplay.setCursor(0, 0)
        self.lcdDisplay.write('LCD Initialized')
        # sleep to display initialization message
        sleep(1)

    def logger_config(self):
        """configure logging settings"""

        # update lcd if linux
        if LINUX:
            self.lcdDisplay.clear()
            self.lcdDisplay.setCursor(0, 0)
            self.lcdDisplay.write('Initializing\n logger...')

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

        if LINUX:
            self.lcdDisplay.clear()
            self.lcdDisplay.setCursor(0, 0)
            self.lcdDisplay.write('Logger\n Initialized.')
            # sleep to display lcd message
            sleep(1)

    def event_loop(self):
        """program loop for controller."""
        self.logger.info("eventLoop has started.")

        # this causes errors ???
        # TODO: add blinking led to application
        # if LINUX:
        # gpio = GPIO(debug=False)
        # led_pin = 13
        #     led_state = gpio.HIGH
        #     gpio.pinMode(led_pin, gpio.OUTPUT)

        # clear lcd
        if LINUX:
            self.lcdDisplay.clear()
            self.lcdDisplay.setCursor(0, 0)

        while True:

            try:
                for tc in self.data_logger.thermocouples:
                    sample_delta = \
                        (datetime.now() - tc.last_sample_time) > timedelta(seconds=tc.tc_settings.sample_interval)

                    log_delta = (datetime.now() - tc.last_log_time) > timedelta(seconds=tc.tc_settings.update_interval)

                    if DEBUG:
                        print 'sample_delta: ' + str(sample_delta)
                        print 'log_delta: ' + str(log_delta)

                    if sample_delta:
                        # update lcd
                        if LINUX:
                            self.lcdDisplay.clear()
                            self.lcdDisplay.setCursor(0, 0)
                            self.lcdDisplay.write('Temp: ' + str(tc.tc_temp))

                        tc.add_temp_history()
                        tc.last_sample_time = datetime.now()

                    if log_delta:
                        tc.store_temperature()
                        tc.last_log_time = datetime.now()

            except Exception as e:
                self.logger.error(e)
            finally:
                # slow the event loop down to interval defined by Settings.py
                # this helps manage processor utilization
                sleep(self.data_logger.event_loop_interval)


if __name__ == "__main__":
    """ Main entry point to program """
    app = Application()