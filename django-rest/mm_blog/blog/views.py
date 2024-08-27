from django.shortcuts import get_object_or_404, get_list_or_404
from http import HTTPMethod

from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from .models import *
from .permissions import IsOwner, IsAdminOwnerOrReadOnly
from .serializers import *
from .search import SearchFiltterMutipleValues
from .filters import FiterPostByHashtagOrHot
import json


class PostView(ModelViewSet):
    serializer_class = PostSerilizerClass
    queryset = BlogPost.objects.all().order_by("-created_at")
    permission_classes = [IsAdminOwnerOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFiltterMutipleValues, OrderingFilter, FiterPostByHashtagOrHot]
    search_fields = ['=title']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=[HTTPMethod.PATCH], serializer_class=CommentSerializerClass, permission_classes=[IsAuthenticated])
    def add_comment(self,  request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            blog_post = BlogPost.objects.get(pk=kwargs['pk'])
            serializer.save(user=request.user, post=blog_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=[HTTPMethod.PATCH])
    def add_vote(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf-8'))
        is_positive = body['is_positive']
        post = get_object_or_404(BlogPost, pk=kwargs['pk'])
        votes = Vote.objects.filter(blog_post=post, user=request.user)

        if not votes.exists():
            Vote.objects.create(user=request.user, blog_post=post, status=is_positive)
        else:
            vote = votes.first()
            if vote.status != is_positive:
                vote.delete()
                Vote.objects.create(user=request.user, blog_post=post, status=is_positive)

        return Response(status=status.HTTP_201_CREATED)


class DeleteHashtagsView(DestroyAPIView):
    serializer_class = HashtagSerializerClass
    queryset = Hashtag.objects.all()
    permission_classes = [IsAdminUser]


class CommentView(ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = CommentSerializerClass
    allowed_methods = [HTTPMethod.GET, HTTPMethod.PUT, HTTPMethod.DELETE]
    queryset = Comment.objects.all()


class VoteOnPost(GenericAPIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = [HTTPMethod.GET]
    serializer_class = VotesSerializerClass

    def get(self, request, **kwargs):
        votes = get_list_or_404(Vote, blog_post__pk=kwargs['pk'])
        serializer = self.get_serializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)