from django.urls import path
from .views import (
    HeartProductView
)

urlpatterns = [
    path('/heart/product',HeartProductView.as_view())
]