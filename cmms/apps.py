from django.apps import AppConfig


class CmmsConfig(AppConfig):
    name = 'cmms'
    def ready(self):
        import cmms.signals
