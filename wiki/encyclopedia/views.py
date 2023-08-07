from django.shortcuts import render
from django import forms
from . import util
from .util import *
import markdown2
import random

#python manage.py runserver
def index(request):
    if request.method == "GET":
        if request.GET != {}:
            #print(request.GET['q']) #breaks "Home" button wihtout if statement.
            if get_entry(request.GET['q']) != None:
                return landingpage(request, title = request.GET['q'])
            else:
                possible_entries = []
                for i in list_entries():
                    if request.GET['q'].lower() in i.lower():
                        possible_entries.append(i)
                return render(request, "encyclopedia/searchresults.html", {
                    'possible_entries': possible_entries
                })


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def landingpage(request, title):

    if get_entry(title) is not None:
        for i in list_entries():
            if title == i.lower():
                title = i #can't say wiki_title = i or else it breaks the app

        return render(request, "encyclopedia/title.html", {
            "title": title, #using diff variable here like wiki_title wont work. referenced before assignment error
            "entry": markdown2.markdown(get_entry(title))
            })
    else:

        return render(request, "encyclopedia/error.html", {
            "message": "404 - The page you are looking for does not exist."
        })

def createnewpage(request):

    if request.method == "POST":

        if get_entry(request.POST['title']) is not None:
            return render(request, "encyclopedia/error.html", {
            "message": "There is already an entry with this title."
        })

        else:
            # have to add a #to the title and add it before the paragraph text ^^
            newdesc = f"#{request.POST['title']} \n" + request.POST['paragraph_text']
            save_entry(request.POST['title'], newdesc)
            return landingpage(request, request.POST['title']) #go to new entry's page (the one that this just created)

    return render(request, "encyclopedia/newpage.html")


def edit(request, title):

    '''The textarea should be pre-populated with the existing Markdown content of the page.
    (i.e., the existing content should be the initial value of the textarea).
    The user should be able to click a button to save the changes made to the entry.
    Once the entry is saved, the user should be redirected back to that entry’s page.'''

    initialdata = get_entry(title)


    if request.method == "POST": #when save is pressed
        print(request.POST)
        save_entry(title, request.POST['updated_text'])
        return landingpage(request, title)

    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'initialdesc': initialdata
    })


def randomm(request):
    title = random.choice(list_entries())
    return landingpage(request, title= title)