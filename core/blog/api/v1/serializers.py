from rest_framework import serializers
from blog.models import Post


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
        fields = ['id', 'title', 'status', 'content', 'created_date', 'published_date']