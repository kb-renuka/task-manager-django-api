from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task, Category
from .serializers import (
    TaskSerializer, TaskListSerializer, CategorySerializer, TaskStatsSerializer
)
from .permissions import IsOwner
from .filters import TaskFilter
from .pagination import StandardResultsPagination


class CategoryViewSet(viewsets.ModelViewSet):
    """
    /api/categories/            GET (list), POST (create)
    /api/categories/{id}/       GET, PUT, PATCH, DELETE
    """
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """
    /api/tasks/                 GET (list, paginated + filterable), POST (create)
    /api/tasks/{id}/             GET, PUT, PATCH, DELETE
    /api/tasks/{id}/complete/    PATCH  — mark a task done
    /api/tasks/{id}/reopen/      PATCH  — move a task back to TODO
    /api/tasks/overdue/          GET    — tasks past due_date and not done
    /api/tasks/stats/            GET    — dashboard counts
    """
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    pagination_class = StandardResultsPagination
    filterset_class = TaskFilter
    search_fields = ('title', 'description')
    ordering_fields = ('due_date', 'created_at', 'priority', 'status')

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).select_related('category')

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'DONE'
        task.completed_at = timezone.now()
        task.save(update_fields=['status', 'completed_at', 'updated_at'])
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['patch'])
    def reopen(self, request, pk=None):
        task = self.get_object()
        task.status = 'TODO'
        task.completed_at = None
        task.save(update_fields=['status', 'completed_at', 'updated_at'])
        return Response(TaskSerializer(task).data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        qs = self.get_queryset().filter(
            due_date__lt=timezone.now()
        ).exclude(status='DONE')
        page = self.paginate_queryset(qs)
        serializer = TaskListSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        qs = self.get_queryset()
        data = {
            'total': qs.count(),
            'todo': qs.filter(status='TODO').count(),
            'in_progress': qs.filter(status='IN_PROGRESS').count(),
            'done': qs.filter(status='DONE').count(),
            'overdue': qs.filter(due_date__lt=timezone.now()).exclude(status='DONE').count(),
            'high_priority_open': qs.filter(priority='HIGH').exclude(status='DONE').count(),
        }
        return Response(TaskStatsSerializer(data).data, status=status.HTTP_200_OK)
