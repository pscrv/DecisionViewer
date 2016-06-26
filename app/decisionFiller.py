"""
Interface to fill in meta and text data of a decision
"""

from .models import Decision
from . import epoSearch, epoConverter

def get_meta(caseNumber, language, forceDownload = False):
    inDB = Decision.objects.filter(CaseNumber = caseNumber, DecisionLanguage = language).first() #there should not be more than one
    if inDB is None or not inDB.MetaDownloaded or forceDownload:
        response = epoSearch.searchCaseNumber(caseNumber)
        decision = epoConverter.metaToDecision(response)
    else:
        decision = inDB
    return decision

def get_text(caseNumber, language, forceDownload = False):
    inDB = Decision.objects.filter(CaseNumber = caseNumber, DecisionLanguage = language).first() #there should be no more than one
    if inDB is None or not inDB.MetaDownloaded:
        inDB = get_meta(caseNumber, language, forceDownload = True)
        
    response = epoSearch.searchDecisionText(inDB.Link)
    decision = epoConverter.textToDecision(response, caseNumber, language)
    return decision

