from rest_framework import serializers
from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'color', 'task_count', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_task_count(self, obj):
        return obj.tasks.count()


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'status', 'priority', 'due_date',
            'category', 'category_name', 'owner', 'is_overdue',
            'completed_at', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'owner', 'completed_at', 'created_at', 'updated_at')

    def validate_category(self, value):
        request = self.context.get('request')
        if value and request and value.owner != request.user:
            raise serializers.ValidationError("You can only assign your own categories.")
        return value


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category_name = serializers.ReadOnlyField(source='category.name')
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'status', 'priority', 'due_date', 'category_name', 'is_overdue')


class TaskStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    todo = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    done = serializers.IntegerField()
    overdue = serializers.IntegerField()
    high_priority_open = serializers.IntegerField()
