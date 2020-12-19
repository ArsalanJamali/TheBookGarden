from django.urls import path
from .views import CheckoutOrderView,getAddressObject

app_name='order_app'


urlpatterns = [
    path('checkout/',CheckoutOrderView,name='checkout-order'),
    path('checkout/getAddress/',getAddressObject,name='get_address_object')
]
