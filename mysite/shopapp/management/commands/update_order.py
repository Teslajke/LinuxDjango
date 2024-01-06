from django.core.management import BaseCommand  # base django class for commands
from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        # get first from db, or None
        order = Order.objects.first()
        if not order:
            self.stdout.write('No order found')
            return

        products = Product.objects.all()

        # many to many
        for product in products:
            # add product to order
            order.products.add(product)
        # save order in db
        order.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Seccessfully added product {order.products.all()} to order {order}')
        )
