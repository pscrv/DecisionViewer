"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import Decision
from .AppState import AppState
from . import epofacade

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)



    return render(
        request,
        'app/index.html',
        {
            'title':'Decision Viewer',
            'decisions':AppState.LatestDecisions,
            'year':AppState.Year,
            'dbsize':AppState.DBSize
        }
    )

def decision_details(request, pk):
    """Renders the decision_details page."""
    assert isinstance(request, HttpRequest)

    try:
        decision = get_object_or_404(Decision.objects, pk = pk)
        decision.FillData()
        citedDecisions = []
        for case in decision.CitedCases_List():
            dec, created = Decision.objects.get_or_create(CaseNumber = case)
            if created:
                dec.CaseNumber = case
                dec.save()
            citedDecisions.append(dec)


    except Decision.DoesNotExist:
        # What are we doing here? Where did we get the pk?
        return redirect(request.META['HTTP_REFERER'])

    return render(
        request,
        'app/decision_details.html',
        { 
            'appstate':AppState,
	        'decision':decision,
            'citedDecisions':citedDecisions,
        }
        )


def search_caseNumber(request):
    """Searches for a case by case number """
    """If not in the DB, then the search will extend the the EPO website"""
    
    if not request.method == 'POST':
        return redirect(request.META['HTTP_REFERER'])

        
    query = request.POST.get('q', None)
    results = Decision.objects.filter(CaseNumber=query)
    if results:
        # Yay, found it in our DB
        return redirect('decision_details', pk = results[0].pk)
    else:
        # Boo, not in our DB yet
        newDecision = epofacade.GetCaseFromNumber(query)
        if newDecision:
            # Yes, got it from the EPO site
            newDecision.save()
            return redirect('decision_details', pk = newDecision.pk)
        else:
            # More boo, even EPO does not have it :-(
            return redirect(request.META['HTTP_REFERER'])
        


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
        )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
