from django.contrib.auth.models import User, Group
#from rest_framework import serializers
from .models import Trip, Bus


#class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']
#
#
# #class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
#
#
# #class TripSerializer(serializers.ModelSerializer):
#     bus = serializers.CharField(source='bus', read_only=True)
#     coach_no = serializers.IntegerField()
#
#     class Meta:
#         model = Trip
#         depth = 2
#
#
# #class BusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bus
#         depth = 2
