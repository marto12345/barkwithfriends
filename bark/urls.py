from django.conf.urls import url
from bark import views
urlpatterns = [

      url(r'^$', views.index, name='index'),
      url(r'about/$', views.about, name='about'),
      url(r'^add-event/$', views.add_event, name='add_event'),
      url(r'^index/$', views.show_event, name='show_event'),
      url(r'^register/$', views.register, name='register'),
      url(r'^dogowner/$', views.register_owner, name='register_owner'),
      url(r'^organizer/$', views.register_organizer, name='register_organizer'),
      url(r'^login/$', views.user_login, name='login'),
]