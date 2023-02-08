from rest_framework import serializers
from applications.post.models import Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'