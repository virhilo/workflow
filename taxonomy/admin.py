# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import Taxonomy


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('term', 'description', )
    list_filter = ('dictionary', )
    search_fields = ('term', 'dictionary__term', 'description', )
    save_as = True
admin.site.register(Taxonomy, TaxonomyAdmin)
