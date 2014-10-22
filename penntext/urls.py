from django.conf.urls import patterns, url
from penntext import views

urlpatterns = patterns('',                        
                        url(r'^$', views.index, name='index'),
                        url(r'^about/', views.about, name='about'),
                        url(r'^register/$', views.register, name = 'register'),
                        url(r'^login/$', views.user_login, name='login'),
                        url(r'^logout/$', views.user_logout, name='logout'),
                        url(r'^my_job/$', views.my_job, name='my_job'),
                        url(r'^(?P<job_name_url>\w+)/job/$', views.joblist, name = 'joblist'),
                        url(r'^(?P<job_name_url>\w+)/add_job/$', views.add_job, name='add_job'),
                        url(r'^confirm/(?P<activation_key>\w+)/$', views.confirm, name = 'confirm'),             
                        url(r'^del/(?P<sell_id>\w+)/$', views.del_flatprice, name = 'del_flatprice'),
                        url(r'^(?P<theid>\w+)/(?P<job_url>\w+)/(?P<job_name_url>\w+)/$', views.accept_job, name = 'accept_job'),             
                        url(r'^my_accepted/$', views.my_accepted, name = 'my_accepted'),
                       )
