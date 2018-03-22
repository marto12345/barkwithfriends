
"""barkwithfriends URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from bark import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^about$',views.about,name='about'),
    url(r'^index$',views.index,name='index'),
    url(r'^food-menu.xml$',views.food_menu,name='food-menu'),
    url(r'^contact$',views.contact,name='contact'),
    url(r'^events$',views.events,name='events'),
    url(r'^add-event$',views.add_event,name='add-event'),
    url(r'^ratings$',views.ratings,name='ratings'),
    url(r'^view-ratings$',views.view_ratings,name='view_ratings'),
    url(r'^add-rating$',views.add_rating,name='add-rating'),
    url(r'^ratings/(?P<organizer_str>\w+)$',views.ratings,name='ratings'),

    url(r'^register$',views.register,name='register'),
    url(r'^login$',views.user_login,name='login'),
    url(r'^reset-password/$', views.reset_password, name='reset_password'),
    url(r'^dogowner/$', views.register_owner, name='register_owner'),
    url(r'^organizer/$', views.register_organizer, name='register_organizer'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^update-profile/', views.update_profile, name='update-profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
