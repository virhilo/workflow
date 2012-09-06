# -*- coding: UTF-8 -*-
from django.db import models
import re

class Taxonomy(models.Model):
    dictionary = models.ForeignKey(
        'self', related_name='%(class)s_dictionary',
        verbose_name=u"Dictionary name",
        help_text=u"Dictionary root element",
    )
    term = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=u"term",
        help_text=u"Short definition of term",
    )
    description = models.CharField(
        max_length=5000,
        blank=True,
        verbose_name=u"description",
        help_text=u"Extended description of term, etc.",
    )
    order = models.IntegerField(
        blank=True,
        null=True,
        help_text=u"Used for custom ordering",
    )
    maps = models.ManyToManyField(
        'self',
        related_name='%(class)s_maps',
        through='TaxonomyMaps',
        symmetrical=False,
        blank=True, null=True,
    )

    objects = models.Manager()
    public = models.Manager()

    class Meta:
        unique_together         = [("dictionary", "term")]
        verbose_name            = u'Słownik'
        verbose_name_plural     = u'Słowniki'
        ordering                = ('dictionary__term', 'order',)

    def __unicode__(self):
        return u'%s' % (self.term)

    def description_view(self):
        '''
        Clear {key:value} tags from description
        '''
        return re.sub(r'\{\w+:[^\}]+\}', '', self.description)

    def extra_view(self):
        '''
        Extract {key:value} to dict.
        '''
        t = {}
        for mo in re.finditer(r'\{(\w+):([^\}]+)\}', self.description):
            t[mo.group(1)] = mo.group(2)
        return t

class TaxonomyFlat(Taxonomy):
    def map_view(self):
        ret = ', '.join(self.maps.values_list('term', flat=True))
        return ret
    def dictionary_view(self):
        return self.dictionary
    class Meta:
        proxy = True

class TaxonomyMaps(models.Model):
    '''
    Used for create subsets related inside taxonomy
    '''
    label = models.ForeignKey(Taxonomy, related_name='%(class)s_label')
    map = models.ForeignKey(Taxonomy, related_name='%(class)s_map')