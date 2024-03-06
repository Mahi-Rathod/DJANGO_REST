from rest_framework import serializers
from .models import *
from .models import User
from .helpers import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','phone','password']
        
    def create(self, validated_data):
        user = User.objects.create(email = validated_data['email'], phone = validated_data['phone'])
        user.set_password(validated_data['password'])
        send_otp_to_mobile(validated_data['phone'],user)
        user.save()
        return user
        