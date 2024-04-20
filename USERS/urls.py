from django.urls import path, include
from .views import signup,login_view,subscribe,logout_view, google_login,google_callback


app_name = "auth"
urlpatterns = [
    path("register",signup,name="register"),
    path("login",login_view,name="login"),
    path("logout",logout_view,name="logout_user"),
    path("subscribe",subscribe,name="subscribe") ,
    path("login/google/",google_login,name="google_login"),
    path('login/google/callback/', google_callback, name='google_callback'),
    # path('password_reset/', include('django.contrib.auth.urls'), name="recovery")
]