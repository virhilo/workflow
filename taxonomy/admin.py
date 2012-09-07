# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext as _
from models import Taxonomy
from wfadmin.admin import wfModelAdmin


class TaxonomyFilter(admin.SimpleListFilter):
    '''
    Filtering taxonomy for specified dictionary from list.
    '''
    title = _('dictionary')
    parameter_name = 'dictionary'
    def lookups(self, request, model_admin):
        return ((u'%s' % lookup[0], lookup[1]) for lookup in\
            Taxonomy.objects.filter(
                Q(
                    dictionary__id=1
                ) | Q(
                    id__in=model_admin.queryset(request).values_list(
                        'dictionary', flat=True,
                    )
                ),
            ).order_by('term').values_list('id', 'term',))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(dictionary__id=self.value())
        return queryset



class TaxonomyInline(admin.TabularInline):
    model = Taxonomy
    extra = 0
    verbose_name = _('dictionary term')
    verbose_name_plural = _('dictionary terms')


class TaxonomyAdmin(wfModelAdmin):
    inlines = [TaxonomyInline, ]
    list_display = ('term', 'description', )
    list_filter = (TaxonomyFilter, )
    search_fields = ('term', 'dictionary__term', 'description', )
    save_as = True

    def queryset(self, request):
        # remove root dict from queryset
        return self.model._default_manager.get_query_set().filter(
            id__gt=1,
        )

admin.site.register(Taxonomy, TaxonomyAdmin)
