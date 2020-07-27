from django.urls import path
from .views import (
    CategoryView,
    LikeView,
    ProductView,
    SpecialOrderView
)

urlpatterns = [
    path('', CategoryView.as_view()),
    path('/like',LikeView.as_view()),
    path('/product',ProductView.as_view()),
    path('/specialorders',SpecialOrderView.as_view())
]