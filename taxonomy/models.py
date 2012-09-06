# -*- coding: UTF-8 -*-
import re
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Taxonomy(models.Model):
    '''
    General taxonomy table, collect data as term:description in primary
    application language
    '''
    dictionary = models.ForeignKey(
        'self',
        related_name='%(class)s_dictionary',
        verbose_name=_('dictionary name'),
        help_text=_('Dictionary root element'),
    )
    term = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('term'),
        help_text=_('Short definition of term'),
    )
    description = models.CharField(
        max_length=5000,
        blank=True,
        verbose_name=('description'),
        help_text=_('Extended description of term, etc.'),
    )
    order = models.IntegerField(
        blank=True, null=True,
        help_text=_('Used for custom ordering'),
    )
    maps = models.ManyToManyField(
        'self',
        blank=True, null=True,
        related_name='%(class)s_maps',
        through='TaxonomyMaps',
        symmetrical=False,
    )

    objects = models.Manager()
    # this is used for compatibility with other webapps where public manager
    # show data accepted for general publish
    public = models.Manager()

    class Meta:
        verbose_name = _('dictionary')
        verbose_name_plural = _('dictionaries')
        unique_together = [('dictionary', 'term', ), ]
        ordering = ('dictionary__term', 'order',)

    def __unicode__(self):
        return u'%s' % (self.term)


class TaxonomyFlat(Taxonomy):
    '''
    String representation of specified dictionary content.
    '''
    class Meta:
        proxy = True

    def map_view(self):
        return u', '.join(self.maps.values_list('term', flat=True))

    def dictionary_view(self):
        return self.dictionary


class TaxonomyMaps(models.Model):
    '''
    Used for create subsets related inside taxonomy.
    '''
    label = models.ForeignKey(Taxonomy, related_name='%(class)s_label')
    map = models.ForeignKey(Taxonomy, related_name='%(class)s_map')
