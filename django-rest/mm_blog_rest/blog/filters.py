from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost


    

class FiterPostByHashtagOrHot(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'hashtag' in request.query_params:
            param = request.query_params.get('hashtag')
            return BlogPost.objects.filter(hashtags__value=param)
        elif 'hot' in request.query_params:
           posts_list = [x.pk for x in BlogPost.objects.all() if x.is_hot == True]
           return BlogPost.objects.filter(pk__in=posts_list)
        
        return super().filter_queryset(request, queryset, view)