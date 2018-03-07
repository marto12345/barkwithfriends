from django.conf.urls import url
from bark import views
urlpatterns = [

      url(r'^$', views.index, name='index'),
      url(r'about/$', views.about, name='about'),
      url(r'^add_category/$', views.add_event, name='add_event'),
      url(r'^index/$', views.show_event, name='show_event'), ]
