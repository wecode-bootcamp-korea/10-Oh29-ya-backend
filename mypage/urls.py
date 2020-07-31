from django.urls import path
from .views      import (
    HeartProductView,
    HeartPostView
)

urlpatterns = [
    path('/heart/product',HeartProductView.as_view()),
    path('/heart/post', HeartPostView.as_view())
]
