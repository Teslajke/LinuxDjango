from django.core.management import BaseCommand  # base django class for commands
from shopapp.models import Product  # to create new data in db


class Command(BaseCommand):
    """
    Creates new products
    """

    def handle(self, *args, **options):
        self.stdout.write("Create products")
        products_names = [
            'Desktop',
            'Laptop',
            'Smartphone'
        ]

        for product_name in products_names:
            product, created = Product.objects.get_or_create(name=product_name)
            # get_or_create method create if not exist or get if exist. It also returns Boolean created. That is why we use product, created
            self.stdout.write(f'Created product {product.name}')

        self.stdout.write(self.style.SUCCESS("Products created"))
