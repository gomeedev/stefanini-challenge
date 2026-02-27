from rest_framework import serializers

from .models import Task, StatusChoice

from user.models import User




class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()

    def get_assigned_to(self, obj):
        if obj.assigned_to:
            return {
                "id": obj.assigned_to.id,
                "first_name": obj.assigned_to.first_name,
                "last_name": obj.assigned_to.last_name,
            }
        return None

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to', 'created', 'updated']


class CreateTaskSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=120)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        from .services import create_task
        return create_task(**validated_data)


class UpdateStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=StatusChoice.choices)

    def update(self, instance, validated_data):
        from .services import update_status
        return update_status(instance.id, validated_data['status'])


class AssignTaskSerializer(serializers.Serializer):
    assigned_to_id = serializers.IntegerField(allow_null=True)

    def update(self, instance, validated_data):
        from .services import assign_task
        return assign_task(instance.id, validated_data['assigned_to_id'])