# users/urls.py
 
from django.urls import path
from users.views import CreateUserViewSet
 
urlpatterns = [
    path('signup/', CreateUserViewSet.as_view({'get':'create'}), name='signup'),
]