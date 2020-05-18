from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Task
from django.forms import TextInput, Textarea
from django.db import models

from django.urls import path

admin.site.site_header = "TODO"
admin.site.site_title = "TODO App"
admin.site.index_title = "Welcome to TODO app"


class TaskInline(admin.TabularInline):
    model = Task
    readonly_fields = ['subtasks_done', 'root_pk']
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'25'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':30})},
    }
    # fieldsets = (
    #     (None, {'fields': ('ordering', ('link_title', 'link_url'))}),
    # )


class LevelListFilter(admin.SimpleListFilter):
    title = 'level'

    parameter_name = 'level'

    def lookups(self, request, model_admin):
        return (
            ('main', '1. Main'),
            ('sub', '2. Sub'),
            ('sub_sub', '3. Sub Sub'),
            ('remaining', '4. Others'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'main':
            return Task.objects.main_tasks(qs=queryset)
        elif value == 'sub':
            return Task.objects.sub_tasks(qs=queryset)
        elif value == 'sub_sub':
            return Task.objects.sub_sub_tasks(qs=queryset)
        elif value == 'remaining':
            return Task.objects.remaining_tasks(qs=queryset)
        return queryset
    
class RootListFilter(admin.SimpleListFilter):
    title = 'root'

    parameter_name = 'root'

    def lookups(self, request, model_admin):
        return [(e.pk, e.name) for e in Task.objects.main_tasks()]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return Task.objects.self_and_children_tasks(int(value), qs=queryset)
        return queryset
        
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        '__str__',
        'parent',
        'due',
        'important',
        'done',
        'subtasks_done',
        'full_name',)
    fieldsets = (
        ('Parent Task', {'fields': (('name', 'parent',),)}),
        ('description', {'fields': ('description',)}),
        ('attrs', {'fields': (('important', 'done',), ('non_completed_tasks', 'subtasks_done',),)}),
    )
    readonly_fields = ['subtasks_done', 'non_completed_tasks', 'root_pk']
    inlines = [TaskInline,]
    list_filter = [
        LevelListFilter,
        RootListFilter,
        'done',
        'subtasks_done',
        'important',
    ]

    def due(self, obj):
        return obj.due
    due.admin_order_field = 'due'
    
    def get_urls(self):
        urls = super(TaskAdmin, self).get_urls()
        my_urls = [path("export/", export)]
        return my_urls + urls

def export(request):
    for e in Task.objects.all():
        e.refresh()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])