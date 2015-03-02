from flask import Flask, jsonify, render_template
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


@app.route('/api/history')
def get_history():
    data_log = []
    try:
        database.connect

        data_log.append({'series': ['tc']})
        for log in DataLog.select():
            json = {
                'x': log.date_time,
                'y': [log.temperature]
            }
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
    temp_data = {}
    try:
        for tc in app_settings.thermocouples:
            temp_data.update({'temp': tc.tc_temp})
    except Exception as e:
        print e
    finally:
        return jsonify(temp_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
