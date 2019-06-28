# 3rd party
from django.apps import AppConfig


class PosConfig(AppConfig):
    name = "pos"
    verbose_name = "Purchase Order System"

    def ready(self):
        from . import signals
