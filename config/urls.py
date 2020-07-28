from django.urls import (
    path,
    include
)

urlpatterns = [
	path('product', include('product.urls')),
    path('media', include('sns.urls')),
    path('account', include('account.urls'))
]
