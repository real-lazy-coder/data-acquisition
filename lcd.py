# pot_touch_led_lcd.py

import time
import math

import pyupm_i2clcd as lcd
import mraa


# analog input - pot
potPin = 0
pot = mraa.Aio(potPin)
potVal = 0
potGrnVal = 0
potBluVal = 0

lightPin = 1
lum = mraa.Aio(lightPin)
lumVal = 0

tmpPin = 2
tmp = mraa.Aio(tmpPin)
tmpVal = 0


# digital output - led
ledPin = mraa.Gpio(4)
ledPin.dir(mraa.DIR_OUT)
ledPin.write(0)

# digital output - buzzer
buzPin = mraa.Gpio(8)
buzPin.dir(mraa.DIR_OUT)
buzPin.write(0)

# digital input - touch
touchPin = mraa.Gpio(3)
touchPin.dir(mraa.DIR_IN)

# display - lcd
lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)
while 1:
    while touchPin.read() == 1:
        # turn led on
        ledPin.write(1)
        time.sleep(3)
        # wait 3 second to get pot value
        # turn buzzer on
        buzPin.write(1)
        time.sleep(1)
        buzPin.write(0)

        # read pot/print/convert to string/display on lcd
        potVal = int(pot.read() * .249)
        lumVal = float(lum.read())
        tmp1Val = float(tmp.read())
        bVal = 3975
        resistanceVal = (1023 - tmp1Val) * 10000 / tmp1Val
        celsiusVal = 1 / (math.log(resistanceVal / 10000) / bVal + 1 / 298.15) - 273.15
        fahrVal = (celsiusVal * (9 / 5)) + 32
        tmpVal = fahrVal

        print "Pot: " + str(potVal) + " Lumens: " + str(lumVal) + " Temp: " + str(tmpVal)

        potStr = "P:" + str(potVal) + "L:" + str(lumVal)
        lcdDisplay.setCursor(0, 0)
        lcdDisplay.setColor(potVal, 0, 0)
        lcdDisplay.write(potStr)

        lumStr = "Temp: " + str(tmpVal)
        lcdDisplay.setCursor(1, 0)
        lcdDisplay.write(lumStr)

        time.sleep(3)
        potgrnVal = int(pot.read() * .249)
        # Print "Green: " + str(potgrnVal)
        lcdDisplay.setColor(potVal, potgrnVal, 0)
        time.sleep(3)
        potbluVal = int(pot.read() * .249)
        # Print "Blue: " + str(potbluVal)
        lcdDisplay.setColor(potVal, potgrnVal, potbluVal)


    # turn led off
    ledPin.write(0)

    # turn buzzer off
    buzPin.write(0)