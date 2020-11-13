from django.urls import path 
from .views import BookListView

app_name="product_app"

urlpatterns = [
    path('<int:pk>/',BookListView.as_view(),name="category_product_list"),
    path('',BookListView.as_view(),name="product_list"),
]
