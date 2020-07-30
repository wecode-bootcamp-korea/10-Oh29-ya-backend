from django.urls import path

from .views import (
    AddView,
    CartView,
    DeleteView,
    UpdateView,
    CountCartView
)

urlpatterns = [
    path('/add',AddView.as_view()),
    path('',CartView.as_view()),
    path('/count',CountCartView.as_view()), 
    path('/delete',DeleteView.as_view()),
    path('/update',UpdateView.as_view())
]