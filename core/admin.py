from django.contrib import admin
from .models import User
# from .models import Article
from .models import Test
# from .models import TConf
# from .models import LinkConf
# from .models import ArticleConf
# from .models import ProjectConf
# from .models import Project
# from .models import Aktuell
# from .models import AktuellConf
# from .models import Link
# from parler.admin import TranslatableAdmin
from django.contrib.auth.admin import UserAdmin

# admin.site.site_header = "Manzoul e. V. Admin"
# admin.site.site_title = "Manzoul e. V. Admin Portal"
# admin.site.index_title = "Welcome to Manzoul e. V."

#
# class LinkInline(admin.TabularInline):
#     model = Link
#     fieldsets = (
#         (None, {'fields': ('ordering', ('link_title', 'link_url'))}),
#     )


@admin.register(User)
class CUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image',)}),
    )
    # fields = super(Comment, self).save(*args, **kwargs)
    # raw_id_fields = ('origin', 'destination')
    # list_display = ('__str__', 'name', 'date', 'pk')




@admin.register(Test)
class testAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pk')
