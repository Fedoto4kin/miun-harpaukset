from django.contrib import admin
from .models import GrammarTable


@admin.register(GrammarTable)
class GrammarTableAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'html_content')
    list_editable = ('order', 'is_published')
