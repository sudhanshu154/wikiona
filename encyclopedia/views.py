from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown2


from . import util
from markdown2 import Markdown

from django import forms

import secrets
from django.urls import reverse

mdr = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    
    entrspg = util.get_entry(title)

    if entrspg is None:
        return render(request,"encyclopedia/error.html", {
            "entrti" : title.lower()
        })
    else:
        return render(request,"encyclopedia/entry.html",{
        "entrti": title.lower(),   
        "title": mdr.convert(entrspg),
             
    })

def search(request):
        
        query = request.GET.get("query").lower()
        entrspg = util.get_entry(query)
        post = [p.lower() for p in util.list_entries()]
        mech = [m for m in post if query in m]
        sbetr = [] 


        if (len(mech) > 0 and query == mech[0]):
            return render(request, "encyclopedia/entry.html", {

                "entrti": query.lower() ,
                "title":mdr.convert(entrspg),
            })
        
        if (query== ""):
            return render(request,"encyclopedia/error.html", {
               "title":query ,
               "entrti":query ,
             })

        
        else:
                for en in util.list_entries():
                    if query.lower() in en.lower():
                        sbetr.append(en)      

                   

                return render(request, "encyclopedia/search.html", {
                    "sub":sbetr,
                    "query":query,
                    "nomech": mech if len(mech) >= 1 else None
           
                })

class newForm(forms.Form):
    title = forms.CharField(label="titel", widget=forms.TextInput(attrs={'class' : 'form-control col-md-10 col-lg-10'}))
    post = forms.CharField(label='Details("in MARKDOWN form")',widget=forms.Textarea(attrs={'class' : 'form-control col-md-10 col-lg-10', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def random(request):
    entrspg = util.list_entries()
    randomEntry = secrets.choice(entrspg)
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={'title': randomEntry}))


def create(request):
    if request.method == "POST":
        form = newForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["post"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("wiki:entry", kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/create.html", {
                "form": form,
                "existing": True,
                "entry": title
                })
        else:
            return render(request, "encyclopedia/create.html", {
            "form": form,
            "existing": False
            })
    else:
        return render(request,"encyclopedia/create.html", {
            "form": newForm(),
            "existing": False
        })    


def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html", {
            "entryTitle": entry    
        })
    else:
        form = newForm()
        form.fields["title"].initial = entry     
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["post"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/create.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial }) 


  


 
            


        


    



    
        



    
#     query= request.GET['query']
#     allposts = util.list_entries()
#     allpost = allposts(title__icontains=query)
#     post= {'allpost':allpost}
#     return render(request,'',post)
#     #  query = request.GET['query']

#     # allpost = util.list_entries().objects.filter(title__icontains = query)

#     # post = {'allpost' : allpost}
    
#     # return render( request , 'encyclopedia/search.html',post)

# # def search(request):
# #     query=request.GET['query']
# #     allPosts= Post.objects.filter(title__icontains=query)
# #     params={'allPosts': allPosts}
# #     return render(request, 'home/search.html', params)