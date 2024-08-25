from django.contrib import admin
from django.urls import path,include
from BlogApp import views

urlpatterns = [
    path("",views.index),
    path("search",views.search,name="search"),
    path('movie', views.movie),
    path('about-us', views.aboutus,name="aboutus"),
    path('contact-us', views.contactus,name="contactus"),
    path('privacy-policy', views.privacypolicy,name="privacypolicy"),
    path('authors', views.authors,name="authors"),
    path('authors/<str:authorsdetails>', views.authorsdetails,name="authorsdetails"),
    path('authors/<str:authorsdetails>/<str:catagories>', views.authorsdetails_catagories,name="authorsdetails_catagories"),
    path('post/tag/<str:tag>',  views.tagResult,name="tagresult"),
    path('post/categorie/<str:categorie>',  views.postByCategorie,name="postbycategorie"),
    path('post/<str:tag>/<str:posturl>',  views.postdetails,name="postdetails"),
    path('autocomplete',  views.autocomplete,name="autocomplete"),
    path('loadmore',  views.loadmore,name="seemore"),
    path('create-post/', views.post_create, name='post_create'),
    path('makeauthor/',views.makeAuthor,name='make_author'),
    path('login/',views.login_as_user,name='login'),
    path('logout/',views.logout_as_user,name='logout'),
    path('signup/',views.register_as_user,name='register'),
    path('userotp/<str:email>',views.user_otp_verify,name='userotp'),

    
   

]
