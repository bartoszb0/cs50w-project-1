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
        return render(request, "encyclopedia/show.html", {
            "title": title,
            "content": markdown(util.get_entry(title))
        })
    

def create(request):
    return render(request, "encyclopedia/create.html")


def random(request):
    random_page = choice(util.list_entries())
    # Pass the title as a second argument to the reverse function
    # When reverse("wiki:show", args=[random_page]) is used, the random_page variable is passed as the title argument to the show function.
    return HttpResponseRedirect(reverse("wiki:show", args=[random_page]))


def search(request):
    # Ignore capitalization
    all_pages = [word.lower() for word in util.list_entries()]
    search_page = request.GET.get('q').lower()

    if search_page in all_pages:
        return HttpResponseRedirect(reverse("wiki:show", args=[search_page]))
    else:
        all_pages = util.list_entries()
        all = []

        for page in all_pages:
            if search_page.lower() in page.lower():
                all.append(page)

        return render(request, "encyclopedia/search.html", {
            "entries": all,
            "search_page": search_page
        })
