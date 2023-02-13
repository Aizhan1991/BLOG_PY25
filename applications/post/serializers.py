from rest_framework import serializers
from applications.post.models import Post, PostImage, Comment

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = '__all__'
        # fields = ('id','image',)
        # exclude =('post',)


class PostSerializers(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(required = False)
    images = PostImageSerializer(many=True, read_only=True)
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

    def create(self, valadated_data):
        post = Post.objects.create(**valadated_data)

        request = self.context.get('request')
        data = request.FILES
        # for i in data.getlist ('images'):
        #     PostImage.objects.create(post=post,image= i)
        image_objects = []
        for i in data.getlist('images'):
            image_objects.append(PostImage(post=post, image=i))
        PostImage.objects.bulk_create(image_objects) #список одним запрозом добавляет 


        return post 



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'