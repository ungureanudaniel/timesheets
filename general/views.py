from django.shortcuts import render

def home(request):
    template = "general/home.html"

    context = {


    }
    return render(request, template, context)

def contact(request):
    template = "general/contact.html"

    context = {


    }
    return render(request, template, context)