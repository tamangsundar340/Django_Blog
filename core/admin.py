from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from core.models import (
    SiteAdmin,
    Member,
    SiteInformation,
    Notice,
    ContactMessage,
    Category,
    Blog,
    BlogComment,
    Newsletter,
)

class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('overview','content',)




# Register your models here.
admin.site.register(SiteAdmin)
admin.site.register(Member)
admin.site.register(SiteInformation)
admin.site.register(Notice)
admin.site.register(ContactMessage)
admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment)
admin.site.register(Newsletter)