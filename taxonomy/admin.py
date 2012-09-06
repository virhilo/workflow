# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib import admin


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('term', 'description', )
    list_filter = ('dictionary', )
    search_fields = ('term', 'dictionary__term', 'description', )
    save_as = True
