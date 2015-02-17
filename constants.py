#!/usr/bin/env python
import platform

# application name
APP_NAME = "application"

# TODO: Detect Edison, Raspberry Pi, Intel Galileo, etc...

# True is linux, False is Windows
PLATFORM = True

__windows = 'Windows'
__linux = 'Linux'
__platform = platform.system()

if __platform is __windows:
    PLATFORM = False
    WINDOWS = True
    LINUX = False
    LOG_LOCATION = "./"
    APP_DB = LOG_LOCATION + APP_NAME + ".db"

if __platform is __linux:
    PLATFORM = True
    WINDOWS = False
    LINUX = True
    LOG_LOCATION = "//media//application//"
    APP_DB = LOG_LOCATION + APP_NAME + ".db"

# debug mode
DEBUG = False