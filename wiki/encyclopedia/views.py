from django.shortcuts import render
from django.middleware import csrf
from markdown import Markdown
import random
from . import util


def convert_html(title: str):
    content = util.get_entry(title)
    markdowner = Markdown()

    # Check if the file Exists00
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = convert_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

def search(request):
    if request.method == "POST":
        question = request.POST["q"]
        content = convert_html(question)
        if content != None:
            return render(request, "encyclopedia/entry.html", {
                "title": question,
                "content": content
        })
        else:
            recomendations = []
            entries =util.list_entries()
            for entry in entries:
                if question .lower() in entry.lower():
                    recomendations.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "recomendations" : recomendations
            })
        
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        double_title = util.get_entry(title)
        if double_title != None:
            return render(request, "encyclopedia/error.html", {
                "message" : "Page Already Exists"
            })
        else:
            util.save_entry(title,content)
            new_content = convert_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content" : new_content
            })
        
def edit(request):
    if request.method == "POST":
        title = request.POST["edit_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        new_content = convert_html(title)
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content" : new_content
            })
    
def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    content = convert_html(random_title)
    return render(request, "encyclopedia/entry.html", {
            "title": random_title,
            "content": content
        })