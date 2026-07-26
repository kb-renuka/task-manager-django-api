from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'color', 'created_at')
    list_filter = ('owner',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'priority', 'due_date', 'is_overdue')
    list_filter = ('status', 'priority', 'owner')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
