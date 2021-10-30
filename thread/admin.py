from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import *

# Register your models here.

admin.site.register(Thread,MarkdownxModelAdmin)
admin.site.register(Sub_thread,MarkdownxModelAdmin)