from flask import Flask, jsonify, render_template
from settings import AppSettings
from models import *
from datetime import datetime
import  time

app = Flask(__name__)

app_settings = AppSettings()


@app.route('/')
def hello_world():
    try:
        return render_template('index.html')
    except Exception as e:
        print e
        return e


@app.route('/api/history')
def get_history():
    data_log = []
    try:
        database.connect

        for log in DataLog.select():
            n = datetime_to_timestamp(log.date_time)*1000
            json = [
                n,
                log.temperature
            ]
            data_log.append(json)

    except Exception as e:
        if DEBUG:
            print e
    finally:
        database.close()
    return jsonify({'log_data': data_log})


@app.route('/api/temp')
def display_temp():
    """
    Retrieves the current temperature from the controller
    :return: float
    """
    temp_data = []
    try:
        for tc in app_settings.thermocouples:
            n = datetime.utcnow()
            unix_time = int(time.mktime(n.timetuple())*1000)
            temp_data.append([unix_time, tc.tc_temp])
    except Exception as e:
        print e
    finally:
        a = jsonify({'temp': temp_data})
        return a


def utc_mktime(utc_tuple):
    """Returns number of seconds elapsed since epoch

    Note that no timezone are taken into consideration.

    utc tuple must be: (year, month, day, hour, minute, second)

    """

    if len(utc_tuple) == 6:
        utc_tuple += (0, 0, 0)
    return time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))


def datetime_to_timestamp(dt):
    """Converts a datetime object to UTC timestamp"""

    return int(utc_mktime(dt.timetuple()))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
