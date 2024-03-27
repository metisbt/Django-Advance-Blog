from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from blog.models import Post
from django.shortcuts import get_object_or_404


@api_view()
def postList(request):
    posts = Post.objects.all()
    serialize = PostSerializer(posts, many=True)
    return Response(serialize.data)

@api_view()
def postDetail(request,id):
    # return 404
    '''
    from rest_framework import status

    try:
        post = Post.objects.get(pk=id)
        serialize = PostSerializer(post)
        return Response(serialize.data)
    except Post.DoesNotExist:
        return Response({"detail":"Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
    '''
    # return 404 better one
    post = get_object_or_404(Post,pk=id)
    serialize = PostSerializer(post)
    return Response(serialize.data)