from rest_framework import serializers
from .models import *
from .utils import *



class HashtagSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['pk', 'value']

class CommentSerializerClass(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    class Meta:
        model = Comment
        fields = [
            "pk", "text"
        ]

class VotesSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            'blog_post_id',
            'status',
            'user_id'
        ]

    

class GetPostSerializerClass(serializers.ModelSerializer):
    hashtags = HashtagSerializerClass(many=True, read_only=True)
    comment_set = CommentSerializerClass(many=True, read_only=True)

    class Meta():
        model = BlogPost
        fields = (
            "pk", "title", "text", "hashtags", "comment_set", "created_at"
        )


class PostSerilizerClass(serializers.ModelSerializer):
    hashtags = serializers.ListField(write_only=True)

    class Meta():
        model = BlogPost
        fields = (
            "title", "text", "hashtags"
        )

    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtags', [])
        instance = BlogPost.objects.create(**validated_data)
        hashtags = self._get_or_create_hashtags(hashtags_data)
        instance.hashtags.set(hashtags)
        return instance
    
    def update(self, instance, validated_data):
        hashtags_from_request = validated_data.pop('hashtags', [])
        hashtags = filter_first_10_hashtags(hashtags_from_request)
        filterd_hashtags = self._get_or_create_hashtags(hashtags)
        instance.hashtags.set(filterd_hashtags)
        return instance


    def to_representation(self, instance):
        return GetPostSerializerClass().to_representation(instance)
    
    def _get_or_create_hashtags(self, hashtags):
        hashtags = filter_first_10_hashtags(hashtags)
        hashtags = [Hashtag.objects.create(value=x) if not Hashtag.objects.filter(value=x).exists() 
                            else Hashtag.objects.filter(value=x).get() for x in hashtags] 
        return hashtags

