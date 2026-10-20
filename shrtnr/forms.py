from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Link
from captcha.fields import CaptchaField
import re


SHORT_RE = re.compile(r'^[a-z0-9-]{1,50}$')
# Shorts that would clash with other routes on the site.
RESERVED_SHORTS = {'admin', 'captcha', 'static', 'favicon.ico', 'robots.txt'}


class LinkForm(forms.Form):
    def clean_short(self):
        short = self.cleaned_data['short'].strip().lower()
        if not short:
            return short
        if not SHORT_RE.match(short):
            raise forms.ValidationError("Use only lowercase letters, digits and dashes (max 50).")
        if short in RESERVED_SHORTS or Link.objects.filter(short__iexact=short).exists():
            raise forms.ValidationError("Short already exists, please pick something else.")
        return short

    def clean_link(self):
        link = self.cleaned_data['link'].strip()
        if '://' not in link:
            link = 'https://' + link
        try:
            URLValidator(schemes=['http', 'https'])(link)
        except ValidationError:
            raise forms.ValidationError("Input is not a valid URL.")
        return link

    link = forms.CharField(max_length=2000, label="Link")
    short = forms.CharField(max_length=50, label="Short", required=False)
    captcha = CaptchaField()
