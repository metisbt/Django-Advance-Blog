from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile
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
    # category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'status', 'content', 'category', 'snippet', 'relative_url', 'absolute_url', 'created_date', 'published_date']
        read_only = ['author']

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj)
    
    def to_representation(self, instance):
        # for get request object that send by user request
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet', None)
            rep.pop('relative_url', None)
            rep.pop('absolute_url', None)
        else:
            rep.pop('content', None)
        rep['category'] = CategorySerializer(instance.category).data
        return rep
    
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id= self.context.get('request').user.id)
        return super().create(validated_data)
