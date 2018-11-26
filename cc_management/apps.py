from django.apps import AppConfig


class CcManagementConfig(AppConfig):
    name = 'cc_management'

    def ready(self):
        import cc_management.signals
