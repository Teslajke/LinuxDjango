from django.contrib import admin
from .models import Product, Order
from django.http import HttpRequest
from django.db.models import QuerySet
from .admin_mixins import ExportAsCSVMixin


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description='Archive products')
def mark_archived(mdeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(mdeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv'
    ]
    inlines = [
        OrderInline,
    ]
    # set fields you want to see for this model
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    # set field whick will be links to objects
    list_display_links = 'pk', 'name'
    # ORDERING
    # if only ne element - should be comma after it. If to elements - no comma needed
    # sort by name in back order, if similar names - sorty by primary key - pk
    ordering = '-name', 'pk'
    # SEARCH
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            # collapse section. wider section
            'classes': ('collapse', 'wide'),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is soft delete',
        })
    ]

    # NEW DESCRIPTION FOR ADMIN
    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInline(admin.StackedInline):
    # DISPLAY ALL CONNECTED PRODUCTS WITH ORDER
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # DISPLAY ALL CONNECTED PRODUCTS WITH ORDER
    inlines = [
        ProductInline
    ]

    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
