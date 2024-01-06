from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    # meta classes in Django - just a configuration
    class Meta:
        # order by name. If there are similar names - then order by price
        ordering = ['name', 'price']

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    # field for money
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    # will auto add this field when product created
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    # # NEW DESCRIPTION FOR ADMIN
    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + '...'

    # reset view of object in admin panel
    def __str__(self) -> str:
        # !r - repreentative view(name in parences)
        return f'Product(pk={self.pk}, name={self.name!r})'


# one to many
class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # n_delete=models.PROTECT - protect from delete order when user deleted
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # django automatically creates many_to_many_table
    # related_name='orders' = how to get orders from Product
    products = models.ManyToManyField(Product, related_name='orders')
