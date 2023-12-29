from .views import shop_index
from django.urls import path

app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='index')

]
