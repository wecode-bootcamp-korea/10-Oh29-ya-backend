from django.urls import path
from .views      import (
    SignUpView,
    SignInView,
    Activate
)

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/activate/<str:uid64>/<str:token>',Activate.as_view())
]
