from django.urls import path
from .views import (
    AddView,
    CartView,
    DeleteView
)

urlpatterns = [
    path('/add',AddView.as_view()),
    path('',CartView.as_view()),
    path('/delete',DeleteView.as_view())
]