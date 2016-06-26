"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import Decision
from .AppState import AppState
from . import epoSearch, epoConverter, decisionFiller

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
            'dbsize':AppState.DBSize,
            'epoContact':AppState.LatestFromEPO
        }
    )

def decision_details(request, cn):
    """Renders the decision_details page."""
    assert isinstance(request, HttpRequest)

    try:
        decision = get_object_or_404(Decision.objects, CaseNumber = cn)
        decision = decisionFiller.get_text(decision.CaseNumber, decision.DecisionLanguage)

        citedDecisions = []
        if not decision.CitedCases == "":
            for case in decision.CitedCases.split(','):
                response = epoSearch.searchCaseNumber(case.strip())
                dec = epoConverter.metaToDecision(response)
                citedDecisions.append(dec)



    except Decision.DoesNotExist:
        return redirect(request.META['HTTP_REFERER'])

    return render(
        request,
        'app/decision_details.html', 
            { 
            'appstate':AppState,
	        'decision':decision,
            'citedDecisions':citedDecisions,
            'facts':decision.Facts.split('\n\n'),
            'reasons':decision.Reasons.split('\n\n'),
            'order':decision.Order.split('\n\n'),
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
            'year':datetime.now().year,
            'GCount':AppState.Count('G'),
            'GCountMeta':AppState.Count('G', withmeta=True),
            'GCountText':AppState.Count('G', withtext=True),
            'RCount':AppState.Count('R'),
            'RCountMeta':AppState.Count('R', withmeta=True),
            'RCountText':AppState.Count('R', withtext=True),
            'JCount':AppState.Count('J'),
            'JCountMeta':AppState.Count('J', withmeta=True),
            'JCountText':AppState.Count('J', withtext=True),
            'TCount':AppState.Count('T'),
            'TCountMeta':AppState.Count('T', withmeta=True),
            'TCountText':AppState.Count('T', withtext=True),
            'TotalCount':AppState.Count(),
            'TotalCountMeta':AppState.Count(withmeta=True),
            'TotalCountText':AppState.Count(withtext=True),
        }
    )
