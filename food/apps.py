from django.apps import AppConfig

class FoodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'food'

    def ready(self):
        from django.contrib.auth.models import User
        def get_cart_count(self):
            from .models import CartItem
            return CartItem.objects.filter(cart_reference__is_paid=False, cart_reference__user=self).count()

        User.add_to_class("get_cart_count", get_cart_count)
