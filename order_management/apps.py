from django.apps import AppConfig

class OrderManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_management'


    def ready(self):
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import Group

        def create_groups(sender, **kwargs):
            Group.objects.get_or_create(name="cafe_staff")
        
        post_migrate.connect(create_groups, sender=self)
        