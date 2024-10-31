from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "myapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.Login.as_view(), name='login_view'),
    path('logout/', views.Logout.as_view(), name='logout_view'),
    path('friends/', views.FriendList.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('password_change/', views.MyPasswordChange.as_view(), name='password_change'),
    path('password_change_done/', views.MyPasswordChangeDone.as_view(), name='password_change_done'),
    path('username_change/', views.update_username, name='username_change'),
    path('useremail_change/', views.update_useremail, name='useremail_change'),
    path('userimage_change/', views.update_userimage, name='userimage_change'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)