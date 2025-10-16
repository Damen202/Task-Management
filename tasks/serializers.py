from urllib import request
from rest_framework import serializers
from .models import Task
from users.serializers import ProfileSerializer 

class TaskSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['owner'] = request.user
        return super().create(validated_data)


    def validate_due_date(self, value):
        from datetime import date
        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value