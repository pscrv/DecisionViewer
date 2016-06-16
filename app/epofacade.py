"""
Interface methods for querying EPO databases
"""
import requests
import re
import datetime
from bs4 import BeautifulSoup
from .models import Decision

# replace these urls by references to app.AppConstants, once their forms been properly worked out
searchUrl = "http://www.epo.org/footer/search.html"
singleDecisionUrl = "http://www.epo.org/law-practice/case-law-appeals/recent/"

languageList = ["DE", "EN", "FR"]
languageSuffixes = {"DE":"d", "EN":"e", "FR":"f"}


#region --- methods for extracting data ---
def SaveSingleCase(caseNumber):    
   
    from app.AppConstants import noPunctionTranslationTable, factFinder, reasonsFinder, orderFinder
    from app.models import Decision
        
    def _parseMeta(soup, name):
        return soup.find('meta', {'name':name})['content']

    def _splitText(text, lang):
        finder = re.compile(
		    '^' + factFinder[lang] + '$' 
		    + '(.*)'
		    + '^' + reasonsFinder[lang] + '$' 
		    + '(.*)'
		    + '^' + orderFinder[lang] + '$'
		    + '(.*)', 
		    re.MULTILINE|re.DOTALL)
        splitText = re.search(finder, text)
        if splitText:
            test= splitText.group(0)
            f = splitText.group(1)
            r = splitText.group(2)
            o = splitText.group(3)
        else:
            f = "Could not parse text. All text is in the Reasons field."
            r = text
            o = "See Reasons."
        return f, r, o


    if not Decision.objects.filter(CaseNumber = caseNumber).exists():

        data = GetSingleCase(caseNumber)

        if data.reason == "Cannot parse this format: " + caseNumber or data.reason == "Not Found":
            return False


        decisionSoup = BeautifulSoup(data.content, "html.parser")

        newDecision = Decision()
        newDecision.CaseNumber = _parseMeta(decisionSoup, 'dg3CSNCase')
        newDecision.Board = _parseMeta(decisionSoup, 'dg3DecisionBoard')
        newDecision.Keywords = _parseMeta(decisionSoup, 'dg3KEY')
        newDecision.Rules = _parseMeta(decisionSoup, 'dg3RuleRef')
        newDecision.Articles = _parseMeta(decisionSoup, 'dg3ArtRef')
        newDecision.ApplicationNumber = _parseMeta(decisionSoup, 'dg3APN')
        newDecision.Applicant = _parseMeta(decisionSoup, 'dg3Applicant')
        newDecision.IPC = _parseMeta(decisionSoup, 'dg3CaseIPC')
        newDecision.Title = _parseMeta(decisionSoup, 'dg3TLE')
        newDecision.ECLI = _parseMeta(decisionSoup, 'dg3ECLI')

        ddate = _parseMeta(decisionSoup, 'dg3DecisionDate')
        odate = _parseMeta(decisionSoup, 'dg3DecisionOnline')
        language =  _parseMeta(decisionSoup, 'dg3DecisionLang')
        newDecision.DecisionDate = datetime.datetime.strptime(ddate, '%d.%m.%Y')
        newDecision.DecisionOnline = datetime.datetime.strptime(odate, '%d.%m.%Y')
        newDecision.Language = language

        textSection = decisionSoup.find(text=factFinder[newDecision.Language]).findPrevious('p').parent
        textParagraphs = textSection.find_all('p')
        text = "".join(para.string.strip() + '\n\n' for para in textParagraphs if not para.string.translate(noPunctionTranslationTable()).strip() == "")
        split = _splitText(text, language)
        newDecision.FactsAndSubmissions = split[0]
        newDecision.Reasons = split[1]
        newDecision.Order = split[2]

        newDecision.save()

        return True #new case savced

    return False #case was already in the DB, was not saved     


def CaseDataToDecision(caseNumber:str, decision:Decision):
       
    from app.AppConstants import noPunctionTranslationTable, factFinder, reasonsFinder, orderFinder
    from app.models import Decision
        
    def _parseMeta(soup, name):
        return soup.find('meta', {'name':name})['content']

    def _splitText(text, lang):
        finder = re.compile(
		    '^' + factFinder[lang] + '$' 
		    + '(.*)'
		    + '^' + reasonsFinder[lang] + '$' 
		    + '(.*)'
		    + '^' + orderFinder[lang] + '$'
		    + '(.*)', 
		    re.MULTILINE|re.DOTALL)
        splitText = re.search(finder, text)
        if splitText:
            test= splitText.group(0)
            f = splitText.group(1)
            r = splitText.group(2)
            o = splitText.group(3)
        else:
            f = "Could not parse text. All text is in the Reasons field."
            r = text
            o = "See Reasons."
        return f, r, o


    data = GetSingleCase(caseNumber)

    if data.reason == "Cannot parse this format: " + caseNumber or data.reason == "Not Found":
        return False

    decisionSoup = BeautifulSoup(data.content, "html.parser")

    decision.CaseNumber = _parseMeta(decisionSoup, 'dg3CSNCase')
    decision.Board = _parseMeta(decisionSoup, 'dg3DecisionBoard')
    decision.Keywords = _parseMeta(decisionSoup, 'dg3KEY')
    decision.Rules = _parseMeta(decisionSoup, 'dg3RuleRef')
    decision.Articles = _parseMeta(decisionSoup, 'dg3ArtRef')
    decision.ApplicationNumber = _parseMeta(decisionSoup, 'dg3APN')
    decision.Applicant = _parseMeta(decisionSoup, 'dg3Applicant')
    decision.IPC = _parseMeta(decisionSoup, 'dg3CaseIPC')
    decision.Title = _parseMeta(decisionSoup, 'dg3TLE')
    decision.ECLI = _parseMeta(decisionSoup, 'dg3ECLI')

    ddate = _parseMeta(decisionSoup, 'dg3DecisionDate')
    odate = _parseMeta(decisionSoup, 'dg3DecisionOnline')
    language =  _parseMeta(decisionSoup, 'dg3DecisionLang')
    decision.DecisionDate = datetime.datetime.strptime(ddate, '%d.%m.%Y')
    decision.DecisionOnline = datetime.datetime.strptime(odate, '%d.%m.%Y')
    decision.Language = language

    textSection = decisionSoup.find(text=factFinder[decision.Language]).findPrevious('p').parent
    textParagraphs = textSection.find_all('p')
    text = "".join(para.string.strip() + '\n\n' for para in textParagraphs if not para.string.translate(noPunctionTranslationTable()).strip() == "")
    split = _splitText(text, language)
    decision.FactsAndSubmissions = split[0]
    decision.Reasons = split[1]
    decision.Order = split[2]

    decision.save()

#endregion




#region --- methods for retrieval ---   
def GetSingleCase(caseNumber):

    badFormat = requests.Response()
    badFormat.reason = "Cannot parse this format: " + caseNumber

    badReturn = requests.Response()
    badReturn.reason = "Not Found"
    
    finder = re.compile(r'^[DGJRTW][_ ]\d{4}/\d{2}$')
    found = re.match(finder, caseNumber)
    if not found:
        return badFormat
        
    response = Search_Response(partial = "dg3CSNCase:" + caseNumber, number = 1)
    soup = BeautifulSoup(response.content, "html.parser")
    caseTag = soup.find('u')

    if not caseTag:
        return badReturn


    response = requests.get(caseTag.string)
    if response.ok:
        return response
    else:
        return badReturn
    



def SearchLatest(number = 10):
    assert isinstance(number, int), "parameter number must be an integer, but  has type " + str(type(number)) 
    assert number > 0, "parameter number must be > 0, but number = " + str(number)
    return SearchByDate(startDate = datetime.date(1900, 1, 1), endDate = datetime.date.today(), number = number)


def SearchByDate(startDate, endDate, number = 1000):
    assert isinstance(startDate, datetime.date), "startDate should be datetime, but was " + str(type(startDate))    
    assert isinstance(endDate, datetime.date), "startDate should be datetime, but was " + str(type(startDate))
    assert startDate <= endDate

    queryString = "inmeta:dg3DecisionDate:" + str(startDate) + ".." + str(endDate)   
    
    return Search_CaseList(query=queryString, language="lang_en|lang_de|lang_fr", number=number)


def SearchByBoard(board, number = 1000):
    assert isinstance(board, str), "parameter board must be a string"
    assert number > 0, "parameter number must be positive"
    assert number <= 1000, "parameter number must be no bigger than 1000"

    finder = re.compile(r'^(\d)\.(\d)\.(\d{2})$')
    found =  re.match(finder, board)
    assert found, "parameter baord must be of the form 3.5.01"

    requiredString = "dg3BOAnDot:" + found.group(1) + found.group(2) + found.group(3)  
    
    return Search_CaseList(required=requiredString, language="lang_en|lang_de|lang_fr", number=number)


def Search_CaseList(query = "", required = "", partial = "", language = None, start = 0, number = 1000):  

    response = Search_Response(query = query, required = required, partial = partial, language = language, start = start, number = number)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all('r')
    decisionList = []
    finder = re.compile(r'([DGJRTW][_ ]\d{4}/\d{2})')
    for res in results:
        caseString = res.t.string
        found = re.search(finder, caseString)
        if found:
            decisionList.append(found.group(1))

    return decisionList


def Search_Response(query = "", required = "", partial = "", language = None, start = 0, number = 1000):
    assert isinstance(query, str), "parameter query must be a string."
    assert isinstance(required, str), "parameter required must be a string."

    payload = {
        "q":query,
        "requiredfields":required,
        "partialfields":partial,
        "lr":language,
        "start":start,
        "num":number,
        "filter":"0",
        "site":"BoA",
        "client":"BoA_AJAX",
        "ie":"latin1",
        "oe":"latin1",
        "entsp":"0",
        "sort":"date:D:R:d1",
        }

    return requests.get(searchUrl, params=payload)

# endregion 
