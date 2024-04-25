from rest_framework import serializers
from Base.models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Profile
        fields = ['first_name','last_name','email','phone_number','password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','first_name','last_name','email','phone_number','profile_pic','followers']