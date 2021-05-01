from django import forms

from .models import BlogPost

class BlogPostForm(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	content = forms.CharField(widget = forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ['title','image','slug','content','publish_date']

	#custom validation of the form
	def clean_title(self, *args, **kwargs):

		#validations for updateview
		instance = self.instance

		title = self.cleaned_data.get('title')
		qs = BlogPost.objects.filter(title__iexact = title) #this compares titles case insensitively.

		#validations for updateview
		if instance is not None:
			qs = qs.exclude(pk = instance.pk)

		if qs.exists():
			raise forms.ValidationError("This title has already been used. Please give a different title.")
		return title
