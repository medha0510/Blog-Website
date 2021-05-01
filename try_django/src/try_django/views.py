from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
	qs = BlogPost.objects.all()[:5]
	context = {"title" : "WELCOME TO TRY DJANGO", "blog_list": qs}
	return render(request,"home.html", context)

def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form = ContactForm()

	context = {
		"title" : "Contact us",
		"form" : form
	}
	return render(request,"form.html", context)

def about(request):
	return render(request,"about.html", {"title" : "Wanna Know about us???"})

def content(request):
	return HttpResponse("<h1>Content Not Yet !!</h1>")

