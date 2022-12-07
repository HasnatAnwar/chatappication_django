from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import *

class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerial(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =  '__all__'


class ConservationSerial(serializers.ModelSerializer):
    class Meta:
        model = Conservation
        fields ='__all__'

class ChatSerial(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields ='__all__'