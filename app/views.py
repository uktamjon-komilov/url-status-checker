from django.shortcuts import render

def list_of_urls(request):
    context = {}
    return render(request, "service/list.html", context)


def add_url(request):
    context = {}
    return render(request, "service/create.html", context)


def update_url(request):
    context = {}
    return render(request, "service/update.html", context)