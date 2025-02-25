from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown import markdown
from . import util
from random import choice


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'name':'title', 'placeholder': 'Enter title'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'name': 'text', 'placeholder': 'Enter Markdown content for the page'}))


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
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]

            all_pages = [word.lower() for word in util.list_entries()]

            if title.lower() in all_pages:
                return render(request, "encyclopedia/error_creating.html", {
                    "title": title
                })
            else:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("wiki:show", args=[title]))

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
            
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewPageForm()
        })


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
        matching_pages = []

        for page in all_pages:
            if search_page.lower() in page.lower():
                matching_pages.append(page)

        return render(request, "encyclopedia/search.html", {
            "entries": matching_pages,
            "search_page": search_page
        })


def edit(request):
    # http://127.0.0.1:8000/wiki/edit doesnt work
    if request.method == "GET":
        title = request.GET.get('title')
        if title is None:
            return render(request, "encyclopedia/error.html", {
                "page_not_found": "TODO"
            })
        elif title not in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "page_not_found": title
            })
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    elif request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get('title')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("wiki:show", args=[title]))
