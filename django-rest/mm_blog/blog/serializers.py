from rest_framework import serializers
from .models import *
from .utils import *



class HashtagSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['value']



class PostSerilizerClass(serializers.ModelSerializer):
    hashtags = HashtagSerializerClass(many=True, read_only=True)
    hashtags_names = serializers.ListField(write_only=True)

    class Meta():
        model = BlogPost
        fields = (
            "title", "text", "hashtags", "hashtags_names"
        )

  
    def create(self, validated_data):
        user = self.context.get('user')
        hashtags_from_request = validated_data.pop('hashtags_names', '')

        hashtags = filter_first_10_hashtags(hashtags_from_request)
        filterd_hashtags = [Hashtag.objects.create(value=x) if not Hashtag.objects.filter(value=x).exists() 
                            else Hashtag.objects.filter(value=x).get() for x in hashtags]    
         
        blog_post = BlogPost.objects.create(user=user, **validated_data)
        blog_post.hashtags.set(filterd_hashtags)
        
        return blog_post