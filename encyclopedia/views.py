from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown import markdown
from . import util
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "page_not_found": title
        })
    else:
        return render(request, f"encyclopedia/show.html", {
            "title": title,
            "content": markdown(util.get_entry(title))
        })
    

def create(request):
    return render(request, "encyclopedia/create.html")


def random(request):
    random_page = choice(util.list_entries())
    # Pass the title as a second argument to the reverse function
    return HttpResponseRedirect(reverse("wiki:show", args=[random_page]))