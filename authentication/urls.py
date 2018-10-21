from django.conf.urls import url, include
from .views import AuthenticationView

urlpatterns = [
    url('', AuthenticationView.as_view())
]
