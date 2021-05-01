
from django.urls import path
from .views import (
	blog_post_create_view,
	##blog_post_detail_page,
	blog_post_detail_view,
	blog_post_list_view,
	blog_post_delete_view,
	blog_post_update_view,
)


urlpatterns = [
    #paths of CRUD views

    #path('blog/', blog_post_detail_page)

    #first we created this path for only integer values
    #path('blog/<int:post_id>/', blog_post_detail_page)

    #now we have changed it to the below one as we created a slug field in our database and this will 
    #accept integer as well as string in our url to make it look better and simpler.
    
    ##path('blog/<str:slug>/', blog_post_detail_page),


    #re_path(r'^blog/(?P<slug>\d+)/$', blog_post_detail_page)

    path('', blog_post_list_view),
    path('<str:slug>/', blog_post_detail_view),
    path('<str:slug>/update/',blog_post_update_view),
    path('<str:slug>/delete/',blog_post_delete_view),
]
