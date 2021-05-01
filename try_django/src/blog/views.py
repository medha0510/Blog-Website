from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.http import Http404 #to raise correct errors for users

from django.shortcuts import render, get_object_or_404,redirect

# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm
from .forms import BlogPostForm


# def blog_post_detail_page(request,slug):
# 	# try:
# 	# 	obj = BlogPost.objects.get(id = post_id)
# 	# except BlogPost.DoesNotExist:  #for handling doesnotexist errors
# 	# 	raise Http404 #for those errors that said type error
# 	# except ValueError:
# 	# 	raise Http404


# 	#filter returns the list og=f objects present in the database.
# 	# queryset = BlogPost.objects.filter(slug = slug)
# 	# if queryset.count() ==0 :
# 	# 	raise Http404
# 	# obj = queryset.first()

# 	obj = get_object_or_404(BlogPost, slug = slug)

# 	template_name = 'blog_post_detail.html'
# 	context = {"object": obj}

# 	return render(request, template_name, context)


#CRUD -> Create Retrieve Update Delete

#GET method is for Retrieve / List
#POST method is for Create / Update / Delete

def	blog_post_list_view(request):
	#list out objects
	#could be search

	# sending a queryset into qs , it will be a list of python objects in our blogPost
	#qs = BlogPost.objects.all()  #this will give list of all the blogposts
	
	#qs = BlogPost.objects.filter(title_icontains='post') #this will filter down to one specific object

	qs = BlogPost.objects.all().published() 
	#
	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()

	template_name = 'blog/list.html'
	context = {'object_list': qs}
	return render(request, template_name,context)

#this is a wrapper around the below function
#@login_required 	#it checks whether the user is logged in and is a valid user or not.
@staff_member_required
def	blog_post_create_view(request):
	#create objects
	#? use a form


	#this was done using BlogPostForm
	# form = BlogPostForm(request.POST or None)
	# if form.is_valid():
	# 	#print(form.cleaned_data)
	# 	obj = BlogPost.objects.create(**form.cleaned_data)
	# 	form = BlogPostForm()
	# template_name = 'form.html'
	# context = {'form': form}
	# return render(request, template_name,context)

	#this is usinfg BlogPostModelForm
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		#form.save()
		obj = form.save(commit=False)

		obj.user = request.user

		obj.save()
		form = BlogPostModelForm()
	template_name = 'form.html'
	context = {'form': form}
	return render(request, template_name,context)

def	blog_post_detail_view(request, slug):
	# 1 object -> detail view (or retrieve view)
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = 'blog/detail.html'
	context = {'object': obj}
	return render(request, template_name,context)


@staff_member_required
def	blog_post_update_view(request, slug):
	# 1 object -> detail view (or retrieve view)
	obj = get_object_or_404(BlogPost, slug = slug)

	form = BlogPostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	template_name = 'form.html'
	context = {'form': form, 'title': f'Update {obj.title}'}
	return render(request, template_name,context)


@staff_member_required
def	blog_post_delete_view(request, slug):
	# 1 object -> detail view (or retrieve view)
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = 'blog/delete.html'

	#for deleting
	if request.method == 'POST':
		obj.delete()
		return redirect("/blog")

	context = {'object': obj}
	return render(request, template_name,context)