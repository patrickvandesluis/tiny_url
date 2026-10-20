from django.conf import settings
from django.db import IntegrityError
from django.db.models import F
from django.shortcuts import render, redirect
from .forms import LinkForm
from .models import Link
import secrets
import string


SHORT_ALPHABET = string.ascii_lowercase + string.digits
SHORT_LENGTH = 8


def get_client_ip(request):
    # nginx sets X-Real-IP to $remote_addr. X-Forwarded-For can be forged
    # by the client, so it is not used.
    return request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR', '')


def random_short():
    while True:
        short = ''.join(secrets.choice(SHORT_ALPHABET) for _ in range(SHORT_LENGTH))
        if not Link.objects.filter(short__iexact=short).exists():
            return short


def index(request):
    context = {}
    if request.method == 'POST':
        context['form'] = LinkForm(request.POST)
        if context['form'].is_valid():
            link = context['form'].cleaned_data["link"]
            short = context['form'].cleaned_data["short"] or random_short()
            try:
                new_url = Link.objects.create(link=link, short=short, ip=get_client_ip(request))
            except IntegrityError:
                context['form'].add_error('short', "Short already exists, please pick something else.")
            else:
                context['url'] = settings.SHORT_URL_BASE + new_url.short
                context['org_url'] = new_url.link
                context['form'] = LinkForm()
    else:
        context['form'] = LinkForm()

    return render(request, 'index.html', context)


def urlRedirect(request, short):
    try:
        data = Link.objects.get(short=short)
    except Link.DoesNotExist:
        return redirect('/')
    Link.objects.filter(pk=data.pk).update(times_used=F('times_used') + 1)
    return redirect(data.link)
