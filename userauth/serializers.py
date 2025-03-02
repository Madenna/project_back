from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)  # Access `full_name` from `User` model
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)  # Access `phone_number` from `User` model

    class Meta:
        model = Profile
        fields = ['profile_photo', 'full_name', 'phone_number', 'city', 'additional_info']  

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def get_profile(self, obj):
        return ProfileSerializer(obj.profile).data if obj.profile else None

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.profile_photo = profile_data.get('profile_photo', profile.profile_photo)
            profile.city = profile_data.get('city', profile.city)
            profile.additional_info = profile_data.get('additional_info', profile.additional_info)
            profile.save()

        return instance