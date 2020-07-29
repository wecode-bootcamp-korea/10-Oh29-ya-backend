from django.urls import path

from .views import (
    PostView,
    LikePostView
)

urlpatterns = [
    path('/recommend', PostView.as_view()),
    path('/recommend/like', LikePostView.as_view()),
]
