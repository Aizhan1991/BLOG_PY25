from rest_framework import serializers
from applications.feedback.models import Like, Rating , Favorit


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'



class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('rating',)


class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Favorit
        fields = '__all__'

    
