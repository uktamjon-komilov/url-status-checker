from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json

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
    context = {"id": _id}

    urls = Url.objects.filter(id = _id)
    if urls.exists():
        url = urls.first()
        context["form"] = UrlForm(instance=url)
    else:
        return redirect("list_of_urls")

    if request.method == "POST":
        form = UrlForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "You have updated a link!", extra_tags="text text-success")
            return redirect("list_of_urls")
        else:
            messages.add_message(request, messages.WARNING, "Update form is not valid!", extra_tags="text text-warning")

    return render(request, "service/update.html", context)


@csrf_exempt
def check_status(request):
    request_data = json.loads(request.body)
    return JsonResponse(json.dumps(request_data))