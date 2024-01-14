# serializers.py
from rest_framework import serializers
from .models import Tasks

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'completed']


class TodoFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['title', 'completed']