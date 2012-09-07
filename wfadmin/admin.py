from django import forms
from django.conf import settings
from django.contrib import admin


class wfAdminForm(forms.ModelForm):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.min.js',
            settings.STATIC_URL + 'wfadmin/js/wfadmin.js',
        )


class wfModelAdmin(admin.ModelAdmin):
    '''
    Extensions for django admin module
    '''
    save_on_top = True
    form = wfAdminForm

    def queryset(self, request):
        # settings objects as default manager
        qs = super(wfModelAdmin, self).queryset(request).model
        return qs.objects

