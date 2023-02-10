from rest_framework import serializers
from applications.post.models import Post


class PostSerializers(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(required = False)
    owner = serializers.ReadOnlyField(source='owner.email')


    class Meta:
        model = Post
        # fields = ('title',)
        fields = '__all__'

    # def to_representation(self, instance):
        # print(instance)
        # print(representation)
        # representation['name'] = 'John'
        # representation['owner'] = instance.owner.email
        # representation['owner'] = instance.owner.email
        # return representation

    # def create(self, valadated_data):
    #     valadated_data['owner'] = self.context['request'].user  #request.user
    #     return super().create(valadated_data)