# -*- coding: UTF-8 -*-
from django.db import models
import re


class Taxonomy(models.Model):
    """
    General taxonomy table, collect data as term:description in primary
    application language
    """
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
        blank=True, null=True,
        help_text=u"Used for custom ordering",
    )
    maps = models.ManyToManyField(
        'self',
        blank=True, null=True,
        related_name='%(class)s_maps',
        through="TaxonomyMaps",
        symmetrical=False,
    )

    objects = models.Manager()
    # this is used for compatibility with other webapps where public manager
    # show data accepted for general publish
    public = models.Manager()

    class Meta:
        verbose_name = u'Dictionary'
        verbose_name_plural = u'Dictionaries'
        unique_together = [("dictionary", "term", ), ]
        ordering = ('dictionary__term', 'order',)

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
    class Meta:
        proxy = True

    def map_view(self):
        ret = ', '.join(self.maps.values_list('term', flat=True))
        return ret

    def dictionary_view(self):
        return self.dictionary


class TaxonomyMaps(models.Model):
    """
    Used for create subsets related inside taxonomy
    """
    label = models.ForeignKey(Taxonomy, related_name='%(class)s_label')
    map = models.ForeignKey(Taxonomy, related_name='%(class)s_map')
