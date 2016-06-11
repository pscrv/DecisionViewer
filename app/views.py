"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import Decision
import populateDB

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if Decision.objects.count() == 0:
        populateDB.GetDecisions()
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Decision Viewer',
            'year':datetime.now().year,
			'month':datetime.now().month - 1,
			'decisions':Decision.objects.all(),
        })
    )

def decision_details(request, pk):
	"""Renders the decision_details page."""
	assert isinstance(request, HttpRequest)
	decision = get_object_or_404(Decision.objects, pk = pk)
	facts = decision.FactsAndSubmissionsInParagraphs()
	reasons = decision.ReasonsInParagraphs()
	order = decision.OrderInParagraphs()
	return render(
		request,
		'app/decision_details.html',
		context_instance = RequestContext(request, 
		{ 
			'decision':decision,
			'facts': facts,
			'reasons':reasons,
			'order': order,
		})
		)



def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
