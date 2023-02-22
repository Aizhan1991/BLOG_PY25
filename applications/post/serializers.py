from rest_framework import serializers
from applications.post.models import Post, PostImage, Comment
from applications.feedback.serializers import LikeSerializer
from applications.feedback.models import Like
from django.db.models import Avg

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
    ikes = LikeSerializer(many=True, read_only=True)


    class Meta:
        model = Post
        # fields = ('title',)
        fields = '__all__'

    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['like_count'] = instance.likes.filter(is_like=True).count()
        # for like in representation['likes']:
        #     if not like['is_like']:
        #         representation['likes'].remove()
   

    #     rating_result = 0
    #     for rating in instance.rating.all():
    #         rating_result += rating.rating
    #         if rating_result:

    #             representation['rating'] = rating_result / instance.ratings.all().count()
    #         else:
    #             representation['rating'] = rating_result



        representation['rating']= instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        return representation




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

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)

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
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'