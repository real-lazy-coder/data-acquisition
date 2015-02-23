from flask import Flask, jsonify
from settings import AppSettings

app = Flask(__name__)

app_settings = AppSettings()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/temp')
def display_temp():
    temp_data = {}
    try:
        for tc in app_settings.thermocouples:
            temp_data.update({'temp': tc.__get_temp})
    except Exception as e:
        print e
    finally:
        return jsonify(temp_data)


if __name__ == '__main__':
    app.run()
