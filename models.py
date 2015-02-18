#!
from peewee import *
from constants import *

# database name from constants.py
DATABASE = APP_DB

# peewee database instance
database = SqliteDatabase('app.db')


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
    tc_name = ForeignKeyField(ThermocoupleSettings)
    date_time = DateTimeField()
    temperature = FloatField()
    uploaded = BooleanField(default=False)

    class Meta:
        order_by = ('tc_name',)


def create_tables():
    """
    Simple utility function to crate tables
    :return: None
    """
    database.connect()
    database.create_tables([Settings, ThermocoupleSettings, DataLog])


if __name__ == '__main__':
    create_tables()