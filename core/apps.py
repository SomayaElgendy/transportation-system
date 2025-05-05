'''This file defines configuration for the 'core' app.
Django uses this to recognize and set up the app correctly during project startup.'''
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
