from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import *

# Register your models here.

admin.site.register(Review,MarkdownxModelAdmin)
admin.site.register(Dormitory,MarkdownxModelAdmin)