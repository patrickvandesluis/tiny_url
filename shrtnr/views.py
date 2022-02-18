from django.shortcuts import render, redirect
from .forms import LinkForm
from .models import Link
import random, string
import re


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def index(request):
    context = {}
    if request.method == 'POST':
        context['form'] = LinkForm(request.POST)
        if context['form'].is_valid():
            link = context['form'].cleaned_data["link"]
            if not link.startswith('http'):
                link = 'http://' + link
            if context['form'].cleaned_data["short"]:
                short = context['form'].cleaned_data["short"]
            else:
                short = ''.join(random.choice(string.ascii_letters) for x in range(10))
            ip = get_client_ip(request)
            new_url = Link(link=link, short=short, ip=ip)
            new_url.save()
            context['url'] = 'https://vandesluis.com/' + new_url.short
            context['org_url'] = new_url.link
    else:
        context['form'] = LinkForm()

    return render(request, 'index.html', context)   


def urlRedirect(request, short):
    try:
        data = Link.objects.get(short=short)
    except Link.DoesNotExist:
        return redirect('/')
    data.times_used += 1
    data.save()
    return redirect(data.link)

