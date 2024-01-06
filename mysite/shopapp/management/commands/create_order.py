from django.core.management import BaseCommand  # base django class for commands
from django.contrib.auth.models import User
from shopapp.models import Order  # to create new data in db


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Create order')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_address='Ul Pushkina, dom 8',
            promocode='SALE123',
            user=user   # django will find primary key of user
        )
        self.stdout.write(f'Created order {order}')
