"""try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from blog.views import (
	blog_post_create_view,
	##blog_post_detail_page,
)
from searches.views import search_view
#importing the function home_page from views 
from .views import (
	home_page,
	contact,
	about,
	content
)

urlpatterns = [

	path('', home_page),

	path('blog-new/',blog_post_create_view),

	path('blog/',include('blog.urls')),  #here, we have included the urls file from our blog app
										#hence, we weill remove the 'blog/' from all the paths in the blog.urls file.
	
	path('search/', search_view),									

    path('admin/', admin.site.urls),
    path('contact/', contact),
    path('about/', about),
    path('content/', content),
]

if settings.DEBUG:

	from django.conf.urls.static import static
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)