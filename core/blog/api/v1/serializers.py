from rest_framework import serializers
from blog.models import Post, Category


# with Serializer
'''
class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
'''

# with ModelSerializer
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'status', 'content', 'created_date', 'published_date']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']