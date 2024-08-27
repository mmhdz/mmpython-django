from django.urls import path, include

from .views import *
from rest_framework import routers

app_name = "blog"

comment_list = CommentView.as_view({
    'get': 'list'
})

comment = CommentView.as_view({
    'put': 'update',
    'delete': 'destroy',
})


route = routers.SimpleRouter()
route.register(r'post', PostView)


urlpatterns = [
    path('post/<int:pk>/comments/', comment_list),
    path('post/<int:pk>/votes/', VoteOnPost.as_view()),
    path('comment/<int:pk>', comment),
    path('hashtag/<int:pk>', DeleteHashtagsView.as_view()),
    path('', include(route.urls)),
]