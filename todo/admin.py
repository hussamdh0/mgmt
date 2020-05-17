from django.contrib import admin
from .models import Task
from django.forms import TextInput, Textarea
from django.db import models

# admin.site.site_header = "Manzoul e. V. Admin"
# admin.site.site_title = "Manzoul e. V. Admin Portal"
# admin.site.index_title = "Welcome to Manzoul e. V."



class TaskInline(admin.TabularInline):
    model = Task
    readonly_fields = ["all_done",]
    
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
    
class ParentListFilter(admin.SimpleListFilter):
    title = 'parent'

    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        return [(e.pk, e.name) for e in Task.objects.main_tasks()]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return Task.objects.self_and_children_tasks(int(value), qs=queryset)
        return queryset
        
@admin.register(Task)
class testAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'parent', 'important', 'done', 'all_done', 'desc',)
    fieldsets = (
        ('Parent Task', {'fields': (('name', 'parent',),)}),
        ('description', {'fields': ('description',)}),
        ('attrs', {'fields': (('important', 'done',), ('non_completed_tasks', 'all_done',),)}),
    )
    readonly_fields = ['all_done', 'non_completed_tasks']
    inlines = [TaskInline,]
    list_filter = [
        LevelListFilter,
        ParentListFilter,
        'done',
        'all_done',
        'important',
    ]
