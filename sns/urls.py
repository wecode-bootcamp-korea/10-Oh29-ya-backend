from django.urls import path

from .views      import PostView

urlpatterns = [
    path('/recommend', PostView.as_view())
]
