from rest_framework import serializers
from blog.models import Post, Category

# *** defined if it depends on request otherwise we can define in model class ***


# with Serializer
'''
class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
'''

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

# with ModelSerializer
class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    # for serializers methods that define here
    absolute_url = serializers.SerializerMethodField()
    
    # display name instead of id for category
    # category = serializers.SlugRelatedField(many=False,slug_field='name', queryset=Category.objects.all())
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'status', 'content', 'snippet', 'relative_url', 'absolute_url', 'created_date', 'published_date']

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj)
    
    def to_representation(self, instance):
        return super().to_representation(instance)
