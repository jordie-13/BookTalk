from django.contrib import admin
from .models import About_Us
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(About_Us)
class About_UsAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)