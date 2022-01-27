from django.urls import path, include
from .views import ResisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('register', ResisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),

]