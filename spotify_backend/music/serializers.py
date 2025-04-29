from rest_framework import serializers
from .models import Song
from .models import Artist

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer) :
    profile_picture = serializers.ImageField(required=False, write_only=True, allow_null=True) 

    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'profile_picture', 'verified', 'monthly_listeners']
        read_only_fields = ['id']

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        artist = Artist.objects.create(**validated_data)

        if profile_picture:
            artist.profile_picture = profile_picture
            artist.save()
        
        return artist
    
    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_picture:
            instance.profile_picture = profile_picture 
            instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.profile_picture:
            representation['profile_picture'] = instance.profile_picture.url
        else:
            representation['profile_picture'] = None
        return representation

