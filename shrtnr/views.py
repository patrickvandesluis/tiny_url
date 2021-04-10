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
    if request.method == 'POST':
        form = LinkForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            link = form.cleaned_data["link"]
            if re.match('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', link):
                short = ''.join(random.choice(string.ascii_letters) for x in range(10))
                ip = get_client_ip(request)
                new_url = Link(link=link, short=short, ip=ip)
                new_url.save()
                return render(request, 'index.html', {
                    'url': request.build_absolute_uri() + new_url.short,
                    'org_url': new_url.link
                    })
            else:
                print('False')
    else:
        form = LinkForm()
    data = Link.objects.all()
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'index.html', context)   


def urlRedirect(request, short):
    data = Link.objects.get(short=short)
    print(data.link)
    return redirect(data.link)

