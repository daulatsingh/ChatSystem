from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url("search/$", views.search, name="search"),
    url("addfriend/(?P<name>.+)/$", views.addFriend, name="addFriend"),
    url("addgroup/$", views.addgroup, name="addGroup"),
    url("adduserrelation/(?P<groupid>.+)/$", views.usergrouprelation, name="adduserrelation"),
    url("chat/(?P<username>.+)/$", views.chat, name="chat"),
    url("chatgroups/(?P<groupid>.+)/$", views.groupchat, name="groupchat"),
    # url('api/messages/<int:sender>/<int:receiver>/$', views.message_list, name='message-detail'),
    url('api/messages/$', views.update_details, name='update-details'),
    url('api/messages-groups/$', views.update_group_details, name='update-group-details'),
    url("addgroup/$", views.addgroup, name="addFriend"),
]
