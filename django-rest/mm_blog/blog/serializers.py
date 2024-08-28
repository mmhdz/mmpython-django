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
    comments = CommentSerializerClass(many=True, read_only=True)
    votes = VotesSerializerClass(many=True, read_only=True)

    class Meta():
        model = BlogPost
        fields = (
            "pk", "title", "text", "hashtags", "comments", "votes", "created_at"
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
        hashtags = validated_data.pop('hashtags', [])
        instance.title = validated_data['title']
        instance.text = validated_data['text']
        instance.save()
        hashtags_objects = self._get_or_create_hashtags(hashtags)
        instance.hashtags.set(hashtags_objects)
        return instance

    def to_representation(self, instance):
        return GetPostSerializerClass().to_representation(instance)

    def _get_or_create_hashtags(self, hashtags):
        hashtags = filter_first_10_hashtags(hashtags)
        hashtags = [Hashtag.objects.create(value=x) if not Hashtag.objects.filter(value=x).exists() 
                            else Hashtag.objects.filter(value=x).get() for x in hashtags] 
        return hashtags

