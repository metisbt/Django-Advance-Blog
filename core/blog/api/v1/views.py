from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from blog.models import Post
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

# function with APIView
'''@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def postList(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serialize = PostSerializer(posts, many=True)
        return Response(serialize.data)
    elif request.method == "POST":
        serialize = PostSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data)'''
    
# class with APIView
"""class postList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    ''' getting a list of posts and creating new post'''
    def get(self,request):
        ''' retrieving a list of posts '''
        posts = Post.objects.all()
        serialize = PostSerializer(posts, many=True)
        return Response(serialize.data)
    
    def post(self,request):
        ''' creating a post with providing data '''
        serialize = PostSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data)"""

# with GenericAPIView
"""class postList(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    ''' getting a list of posts and creating new post'''
    def get(self,request):
        ''' retrieving a list of posts '''
        queryset = self.get_queryset()
        serialize = self.serializer_class(queryset, many=True)
        return Response(serialize.data)
    
    def post(self,request):
        ''' creating a post with providing data '''
        serialize = self.serializer_class(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data)"""


# with ListCreateAPIView is better
class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    

# function with APIView
"""@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postDetail(request,id):
    # return 404
    '''
    try:
        post = Post.objects.get(pk=id)
        serialize = PostSerializer(post)
        return Response(serialize.data)
    except Post.DoesNotExist:
        return Response({"detail":"Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
    '''
    # return 404 better one
    post = get_object_or_404(Post,pk=id)
    if request.method == "GET":
        serialize = PostSerializer(post)
        return Response(serialize.data)
    elif request.method == "PUT":
        serialize = PostSerializer(post,data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail":"item removed successfully"},status=status.HTTP_204_NO_CONTENT)"""
    
# class with APIView
"""class PostDetail(APIView):
    ''' getting detail of the post and edit plus delete it'''
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, id):
        ''' retrieving the post data '''
        post = get_object_or_404(Post,pk=id)
        serialize = self.serializer_class(post)
        return Response(serialize.data)
    
    def put(self, request, id):
        ''' editing the post data '''
        post = get_object_or_404(Post,pk=id)
        serialize = self.serializer_class(post,data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()

    def delete(self, request, id):
        ''' deleting the post object '''
        post = get_object_or_404(Post,pk=id)
        post.delete()
        return Response({"detail":"item removed successfully"},status=status.HTTP_204_NO_CONTENT)"""

# with RetrieveUpdateDestroyAPIView is better
class PostDetail(RetrieveUpdateDestroyAPIView):
    ''' getting detail of the post and edit plus delete it'''
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object)
        return Response(serializer.data)
    
    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass