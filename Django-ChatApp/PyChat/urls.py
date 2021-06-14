from django.contrib import admin
from django.conf.urls import url, include
from registration import views as rv

urlpatterns = [
    url('admin/', admin.site.urls),
    url('signup/', rv.SignUp, name="register"),
    url(r'^', include("django.contrib.auth.urls")),
    url(r'^', include("chat.urls")),

]
