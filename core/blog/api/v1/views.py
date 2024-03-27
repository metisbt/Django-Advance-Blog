from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from blog.models import Post
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(["GET", "POST"])
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
        return Response(serialize.data)


@api_view(["GET", "PUT", "DELETE"])
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
        return Response({"detail":"item removed successfully"},status=status.HTTP_204_NO_CONTENT)