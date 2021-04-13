from django import forms
from .models import Link
import re


class LinkForm(forms.Form):
    def clean_short(self):
        short = self.cleaned_data['short']
        if Link.objects.filter(short=short).exists():
            raise forms.ValidationError("Short already exists, please pick something else.")
        return short
    def clean_link(self):
        link = self.cleaned_data['link']
        if not re.match('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', link):
            raise forms.ValidationError("Input is not a valid URL.")
        return link
    link = forms.CharField(max_length=5000, label="Link")
    short = forms.CharField(max_length=200, label="Short", required=False)

