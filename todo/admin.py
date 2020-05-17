from django.contrib import admin
from .models import Task

# admin.site.site_header = "Manzoul e. V. Admin"
# admin.site.site_title = "Manzoul e. V. Admin Portal"
# admin.site.index_title = "Welcome to Manzoul e. V."



class TaskInline(admin.TabularInline):
    model = Task
    readonly_fields = ["all_done",]
    # fieldsets = (
    #     (None, {'fields': ('ordering', ('link_title', 'link_url'))}),
    # )


@admin.register(Task)
class testAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'parent', 'important', 'done', 'all_done', 'desc')
    fieldsets = (
        ('Parent Task', {'fields': ('parent',)}),
        ('attrs', {'fields': ('name', ('important', 'done', 'all_done'),)}),
        ('description', {'fields': ('description',)}),
    )
    readonly_fields = ["all_done",]
    inlines = [TaskInline,]
