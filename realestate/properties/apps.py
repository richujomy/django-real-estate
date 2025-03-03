from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.db import connection


def enable_foreign_keys(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        connection_created.connect(enable_foreign_keys)
