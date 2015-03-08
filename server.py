from datetime import datetime
import time

from flask import Flask, jsonify, render_template, request

from settings import AppSettings
from models import *


app = Flask(__name__)

app_settings = AppSettings()


@app.route('/')
def hello_world():
    try:
        return render_template('index.html')
    except Exception as e:
        print e
        return e


@app.route('/api/temp/history')
def get_history():
    data_log = []
    try:
        database.connect

        for log in DataLog.select():
            n = datetime_to_timestamp(log.date_time) * 1000
            json = [
                n,
                two_place_decimal(log.temperature)
            ]
            data_log.append(json)

    except Exception as e:
        if DEBUG:
            print e
    finally:
        database.close()
    return jsonify({'log_data': data_log})


@app.route('/api/temp/history/search')
def api_history_search():
    search_min = request.args.get('min')
    search_max = request.args.get('max')

    # check if min and max have value
    if search_min is None or search_max is None:
        return 'query string error'

    # convert min and max to epoch seconds from epoch milliseconds
    min_seconds = int(search_min) / 1000
    max_seconds = int(search_max) / 1000

    min_datetime = datetime.utcfromtimestamp(min_seconds)
    max_datetime = datetime.utcfromtimestamp(max_seconds)

    data_log = []
    try:
        database.connect

        for log in DataLog.select().where((DataLog.date_time >= min_datetime) & (DataLog.date_time <= max_datetime)):
            n = datetime_to_timestamp(log.date_time) * 1000
            json = [
                n,
                two_place_decimal(log.temperature)
            ]
            data_log.append(json)

    except Exception as e:
        if DEBUG:
            print e
    finally:
        database.close()
    return jsonify({'log_data': data_log})


@app.route('/api/temp/last_log_point')
def last_log_point():
    """
    :return: Last point in sql database
    """
    point = []
    try:
        database.connect()
        p = DataLog.select().order_by(DataLog.id.desc()).get()
        point.append(datetime_to_timestamp(p.date_time) * 1000)
        point.append(two_place_decimal(p.temperature))
    except Exception as e:
        return e
    finally:
        database.close()
    return jsonify({'point': point})


@app.route('/api/temp')
def display_temp():
    """
    Retrieves the current temperature from the controller
    :return: float
    """
    temp_data = []
    try:
        for tc in app_settings.thermocouples:
            # n = datetime.utcnow()
            # unix_time = int(time.mktime(n.timetuple())*1000)
            # convert the time to unix time in milliseconds
            unix_time = datetime_to_timestamp(datetime.now()) * 1000
            temp_data.append([unix_time, two_place_decimal(tc.tc_temp)])
    except Exception as e:
        print e
    finally:
        a = jsonify({'temp': temp_data})
        return a


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/settings/reboot')
def reboot():
    """
    Reboot the operating system
    """
    # TODO: Write reboot code
    return 'Rebooting Unit...'


@app.route('/settings/wifi')
def wifi_setup():
    """
    Setup wifi on device
    """
    return 'Setup wifi...'

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


def two_place_decimal(f_point):
    """
    :return: float with 2 place decimal
    """
    return float("{0:.2f}".format(f_point))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
