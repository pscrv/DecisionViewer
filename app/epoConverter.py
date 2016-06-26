"""
Interface for converting responses from epoSearch to useful data
"""

import re
import string
import datetime
from bs4 import BeautifulSoup, element
from .models import Decision
from . import epoSearch

CASENUMBERFINDER = r'([DGJRTW][_ ]\d{4}/\d{2})'


def toCaseList(response):
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all('r')
    decisionList = []
    finder = re.compile(CASENUMBERFINDER)
    for res in results:
        caseString = res.t.string
        found = re.search(finder, caseString)
        if found:
            decisionList.append(found.group(1))

    return decisionList


def toDecisionList(response):
    caseList = toCaseList(response)
    decisionList = []
    for case in caseList:
        decisionResponse = epoSearch.searchCaseNumber(case)
        decision = metaToDecision(decisionResponse)
        decisionList.append(decision)
    return decisionList



def metaToDecision(response):    
    soup = BeautifulSoup(response.text, "html.parser")

    #Get proceedings case number and proceedings language
    #And create or update a decision
    caseNumber = _parseMeta(soup, 'dg3CSNCase')
    procedureLanguage = _parseMeta(soup, 'dg3DecisionPRL')
    decision = Decision.objects.create_or_update(caseNumber, procedureLanguage)
    
    if decision is None: #will happen if we cannot extract a usable caseNumber or procedureLanguage
        return decision

    #Find a result that has the decision in this language
    theResult = None
    results = soup.find_all("r")
    for res in results:
        decisionLanguage = _parseMeta(res, 'dg3DecisionLang')
        if decisionLanguage == procedureLanguage:
            theResult = res
            break

    if theResult is None:
        theResult = results[0]  # no decision in the language of proceedings? Weird. Take whatever is first
         
    decision = _extractFromMeta(theResult)
    return decision


def _extractFromMeta(tag):
    caseNumber = _parseMeta(tag, 'dg3CSNCase')
    decisionLanguage = _parseMeta(tag, 'dg3DecisionLang')
    metaDictionary = parseToMetaDictionary(tag)
    decision = Decision.objects.create_or_update(caseNumber, decisionLanguage, **metaDictionary)
    return decision


def parseToMetaDictionary(tag):

    ddate = _parseMeta(tag, 'dg3DecisionDate')
    odate = _parseMeta(tag, 'dg3DecisionOnline')

    hw = _parseMeta(tag, 'DC.title')
    finder = re.compile(r'\((.*)\)')
    found = re.search(finder, hw)
    if found:
        hw = found.group(1)
    else:
        hw = ""

    metaDictionary = {
        'DecisionDate': datetime.datetime.strptime(ddate, '%d.%m.%Y'),       
        'DecisionOnline': datetime.datetime.strptime(odate, '%d.%m.%Y'), 
        'Applicant': _parseMeta(tag, 'dg3Applicant'),
        'Opponents': _parseMeta(tag, 'dg3Opponent'),
        'ApplicationNumber': _parseMeta(tag, 'dg3APN'),
        'IPC': _parseMeta(tag, 'dg3CaseIPC'),
        'Title': _parseMeta(tag, 'dg3TLE'),
        'Headword': hw,
        'Board': _parseMeta(tag, 'dg3DecisionBoard'),
        'Keywords': _parseMeta(tag, 'dg3KEY'),
        'Articles': _parseMeta(tag, 'dg3ArtRef'),
        'Rules': _parseMeta(tag, 'dg3RuleRef'),
        'ECLI': _parseMeta(tag, 'dg3ECLI'),
        'CitedCases': _parseMeta(tag, 'dg3aDCI'),
        'Distribution': _parseMeta(tag, 'dg3DecisionDistributionKey'),
        'ProcedureLanguage': _parseMeta(tag, 'dg3DecisionLang'),
        'PDFLink': _parseMeta(tag, 'dg3DecisionPDF'),
        'Link': tag.u.string,
        'MetaDownloaded': True,
        }

    return metaDictionary


            
def _parseMeta(soup, name):
    tag = soup.find('mt', {'n':name})
    if not tag:
        return ""

    v = tag['v'].strip(string.whitespace)
    w = v.strip(string.punctuation + string.whitespace)
    if w == "":
        return w
    else:
        return v



def textToDecision(response, caseNumber, procedureLanguage):
    
    textDictionary = parseToTextDictionary(response)
    decision = Decision.objects.create_or_update(caseNumber, procedureLanguage, **textDictionary)
    return decision


def _loopToHeader(textList, para):
    while para:
        textList.append(para)
        para = para.nextSibling
        if para:
            nextSib = para.nextSibling
            if not nextSib or nextSib.find('b'):    
                textList.append(para)                    
                return textList
            else:
                pass # there is still at least one <p>
        else:
            return textList # we have just dealt with the last <p>   


def parseToTextDictionary(response):        
    soup = BeautifulSoup(response.content, "html.parser")

    textSection = soup.find('div', {'id':'body'})
    if not textSection:
        return

    # strip out all tags other than <p>
    for tag in textSection.children:
        if isinstance(tag, element.Tag):
            if not tag.name == 'p':
                tag.decompose()
        elif tag.string == '\n':
            del tag


    # Now, textSection is a <div/> that contains the facts, reaons, order, 
    # or whatever they are called in our decision.
    # Try to find the secions by looking for <b> tags

        
    headers = textSection.find_all('b')
    if not len(headers) == 3:
        parseDictionary = {
            'FactsHeader': "See Reasons",
            'Facts':  "",
            'ReasonsHeader': "",
            'Reasons':_parasToString(textSection.find_all('p')),
            'OrderHeader': "See Reasons",
            'Order': "",
            'TextDownloaded': True,
            'HasSplitText': False,
            }          
        
    else:
        parseDictionary = {
            'FactsHeader': headers[0].string,
            'Facts': _parasToString(_loopToHeader([], headers[0].parent.nextSibling)),
            'ReasonsHeader': headers[1].string,
            'Reasons': _parasToString(_loopToHeader([], headers[1].parent.nextSibling)),
            'OrderHeader': headers[2].string,
            'Order': _parasToString(_loopToHeader([], headers[2].parent.nextSibling)),
            'TextDownloaded': True,
            'HasSplitText': True,
            }

    return parseDictionary


def _parasToString(paraList):        
        #text = "\n\n".join(para.string.strip() for para in paraList if not para.string.translate(noPunctionTranslationTable()).strip() == "")        
        text = "\n\n".join(para.string.strip() for para in paraList if not para.string.strip(string.whitespace + string.punctuation) == "")
        return text        
    

