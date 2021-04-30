from django.apps import AppConfig


class FoodieConfig(AppConfig):
    name = 'Foodie'

    def ready(self):
        import Foodie.signals