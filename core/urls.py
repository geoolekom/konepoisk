from django.conf.urls import url
from core.views import RegisterView, ConfirmView, UserInfoView, LoginView
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^register/', RegisterView.as_view(), name="register"),
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', logout, {'next_page': '/'}, name="logout"),
    url(r'^confirm/(?P<secret>.+)', ConfirmView.as_view(), name='confirm'),
    url(r'^user/(?P<pk>\d+)', UserInfoView.as_view(), name='user'),
]