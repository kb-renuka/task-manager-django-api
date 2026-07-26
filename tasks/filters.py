import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    category = django_filters.NumberFilter(field_name='category__id')
    due_before = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    due_after = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'category', 'due_before', 'due_after', 'created_after']
