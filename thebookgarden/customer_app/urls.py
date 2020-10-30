from django.urls import path
from .views import SignUpView,SignInView

app_name='customer_app'

urlpatterns = [
    path('register/',SignUpView.as_view(),name='register'),
    path('login/',SignInView.as_view(),name="login")
]
