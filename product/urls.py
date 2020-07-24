from django.urls import path
from .views import (
    ProductView,
    LikeView
)

urlpatterns = [
    path('/', ProductView.as_view()),
    path('/like',LikeView.as_view())
]