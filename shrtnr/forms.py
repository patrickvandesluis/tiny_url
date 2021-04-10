from django import forms


class LinkForm(forms.Form):
    link = forms.CharField(max_length=5000, label="LINK")
    short = forms.CharField(max_length=200, label="SHORT", required=False)
