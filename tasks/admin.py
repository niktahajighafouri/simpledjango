# tasks/admin.py
from django.contrib import admin
from .models import Task, SubTask


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  # Number of empty forms for new subtasks
    fields = ('title', 'description', 'status')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'assigned_to', 'created_by', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'due_date', 'assigned_to', 'created_by')
    search_fields = ('title', 'description', 'assigned_to__username', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Details', {
            'fields': ('status', 'priority', 'due_date', 'assigned_to', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'created_at')
    list_filter = ('status', 'task__title')
    search_fields = ('title', 'description', 'task__title')
    readonly_fields = ('created_at', 'updated_at')
