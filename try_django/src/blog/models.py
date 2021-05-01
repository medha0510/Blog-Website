from django.conf import settings  #to impoet the user model

from django.db import models
from django.db.models import Q
from django.utils import timezone
# Create your models here.

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(publish_date__lte=now)

	def search(self, query):
		lookup = (
					Q(title__icontains=query) |
			        Q(content__icontains=query) |
			        Q(slug__icontains=query) |
			        Q(user__first_name__icontains=query) |
			        Q(user__last_name__icontains=query) |
			        Q(user__username__icontains=query)
			     )
		return self.filter(lookup)


class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().published().search(query)

class BlogPost(models.Model):
	
	#to join to models together, as done in case of tables
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	# this will help set all the related values of a particular row as null when that row is deleted.

	#for uploading images
	image = models.ImageField(upload_to ='image/', blank=True, null=True)


	#we do not want textfield as the title's textaera
	##title = models.TextField()
	#so changing it to charfield with max characters as 120
	title = models.CharField(max_length = 120)
	slug = models.SlugField(unique = True) #hello world -> hello-world
	content = models.TextField(null=True, blank=True)

	#to give publish date
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = BlogPostManager()

	class Meta:
		ordering = ['-publish_date', '-updated', '-timestamp']

	#setting up navigations i.e. links to go from title to its content in the list view
	def get_absolute_url(self):
		return f"/blog/{self.slug}"

	def get_update_url(self):
		return f"{self.get_absolute_url()}/update"

	def get_delete_url(self):
		return f"{self.get_absolute_url()}/delete"