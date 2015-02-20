#!/usr/bin/env python
from peewee import *
from constants import *

# database name from constants.py
DATABASE = APP_DB

# peewee database instance
database = SqliteDatabase(APP_DB)


class BaseModel(Model):
    class Meta:
        database = database


class Settings(BaseModel):
    name = CharField(unique=True)
    description = TextField()
    value = CharField()

    class Meta:
        order_by = ('name',)


class ThermocoupleSettings(BaseModel):
    name = CharField(unique=True)
    description = TextField()
    do = IntegerField()
    ck = IntegerField()
    clk = IntegerField()
    update_interval = FloatField()
    sample_interval = FloatField()

    class Meta:
        order_by = ('name',)


class DataLog(BaseModel):
    tc = ForeignKeyField(ThermocoupleSettings)
    date_time = DateTimeField()
    temperature = FloatField()
    uploaded = BooleanField(default=False)

    class Meta:
        order_by = ('tc',)


def create_tables():
    """
    Simple utility function to crate tables
    :return: None
    """
    database.connect()  # connect to the database via peewee ORM
    database.drop_tables([Settings, ThermocoupleSettings, DataLog], safe=True)  # delete all records in settings
    database.create_tables([Settings, ThermocoupleSettings, DataLog], safe=True)  # create the tables
    database.close()  # close the database connection


def populate_database():
    """
    Populate the database
    :return:
    """
    database.connect()

    # Settings table
    # app_name setting
    setting_1 = Settings(name='app_name', description='Application Name', value='Data Acquisition')

    # event_loop_interval setting
    setting_2 = Settings(name='event_loop_interval',
                         description='Event Loop Timer for delaying the event loop each cycle', value=0.25)

    setting_1.save()  # save setting to database
    setting_2.save()  # save setting to database

    # Thermocouple table
    thermocouple_1 = ThermocoupleSettings(name='freezer', description='freezer thermocouple', do=3, ck=4, clk=5,
                                          update_interval=55, sample_interval=5)

    thermocouple_1.save()  # save thermocouple to database

    database.close()  # close the database connection

    for setting in Settings.select():
        print 'Setting Name\t' + setting.name + '\tSetting Description:\t' + setting.description \
              + '\tSetting Value:\t' + setting.value


if __name__ == '__main__':
    create_tables()
    populate_database()