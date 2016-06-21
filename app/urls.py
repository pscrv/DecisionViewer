"""
Definition of urls for the Decisions Viewer app.
"""

from datetime import datetime
from django.conf.urls import patterns, url, include
from django.contrib.auth.views import login, logout
from app.forms import BootstrapAuthenticationForm
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^decision_details/(?P<pk>.+)/$', views.decision_details, name='decision_details'),
    url(r'^search_caseNumber$', views.search_caseNumber, name='search_caseNumber'),
	url(r'^contact$', views.contact, name='contact'),
	url(r'^about', views.about, name='about'),
	url(r'^login/$',
		login,
		{
			'template_name': 'app/login.html',
			'authentication_form': BootstrapAuthenticationForm,
			'extra_context':
			{
				'title':'Log in',
				'year':datetime.now().year,
			}
		},
		name='login'),
	url(r'^logout$',
		logout,
		{
			'next_page': '/',		},
		name='logout'),
	]

