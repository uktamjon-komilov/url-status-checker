from django.conf.urls import url
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Url

def list_of_urls(request):
    context = {}
    if request.GET.get("action", None) == "delete":
        try:
            _id = int(request.GET.get("id"))
            urls = Url.objects.filter(id=_id)
            if urls.exists():
                urls.delete()
            return redirect("list_of_urls")
        except:
            return redirect("list_of_urls")

    urls = Url.objects.filter(user=request.user).all()
    context["urls"] = urls
    return render(request, "service/list.html", context)


def add_url(request):
    if request.method == "POST":
        url_obj = Url()

        title = request.POST.get("title", None)
        if title:
            url_obj.custom_name = title
        
        url = request.POST.get("url", None)
        if url:
            url_obj.url = url
        
        interval = request.POST.get("request-interval", None)
        if interval:
            url_obj.request_interval = int(interval)
        
        url_obj.user = request.user
        url_obj.save()

        messages.add_message(request, messages.SUCCESS, "You have added a new link to be observed!", extra_tags="text text-success")

        return redirect("list_of_urls")

    return render(request, "service/create.html")


def update_url(request, _id):
    context = {}

    urls = Url.objects.filter(id = _id)
    if urls.exists():
        obj = urls.first()
        context["obj"] = obj
    else:
        return redirect("list_of_urls")

    if request.method == "POST":
        title = request.POST.get("title", None)
        if title:
            obj.custom_name = title
        
        url = request.POST.get("url", None)
        if url:
            obj.url = url
        
        interval = request.POST.get("request-interval", None)
        if interval:
            obj.request_interval = int(interval)
        
        obj.user = request.user
        obj.save()

        messages.add_message(request, messages.SUCCESS, "You have updated a link!", extra_tags="text text-success")

        return redirect("list_of_urls")

    return render(request, "service/update.html", context)