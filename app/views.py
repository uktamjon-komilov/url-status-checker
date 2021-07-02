from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Url
from .forms import UrlForm


@login_required(login_url="/account/login/")
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


@login_required(login_url="/account/login/")
def add_url(request):
    context = {}

    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "You have added a new link to be observed!", extra_tags="text text-success")
            return redirect("list_of_urls")
        else:
            messages.add_message(request, messages.WARNING, "Form you have submitted is not valid!", extra_tags="text text-danger")
            context["form"] = form
            print(form.errors)
            return render(request, "service/create.html", context)
    else:
        context["form"] = UrlForm(initial={"user": request.user})

    return render(request, "service/create.html", context)


@login_required(login_url="/account/login/")
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