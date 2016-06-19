"""
Interface methods for querying EPO databases
"""
import requests
import re
import datetime
import string
from bs4 import BeautifulSoup

# replace these urls by references to app.AppConstants, once their forms been properly worked out
searchUrl = "http://www.epo.org/footer/search.html"
singleDecisionUrl = "http://www.epo.org/law-practice/case-law-appeals/recent/"

languageList = ["DE", "EN", "FR"]
languageSuffixes = {"DE":"d", "EN":"e", "FR":"f"}


#region --- methods for extracting data ---
def CaseMetaToDecision(tag):
       
    from app.models import Decision
        
    def _parseMeta(soup, name):
        return soup.find('mt', {'n':name})['v']      
    
    decision = Decision()
    decision.CaseNumber = _parseMeta(tag, 'dg3CSNCase')
    decision.Board = _parseMeta(tag, 'dg3DecisionBoard')
    decision.Keywords = _parseMeta(tag, 'dg3KEY')
    decision.Rules = _parseMeta(tag, 'dg3RuleRef')
    decision.Articles = _parseMeta(tag, 'dg3ArtRef')
    decision.ApplicationNumber = _parseMeta(tag, 'dg3APN')
    decision.Applicant = _parseMeta(tag, 'dg3Applicant')
    decision.IPC = _parseMeta(tag, 'dg3CaseIPC')
    decision.Title = _parseMeta(tag, 'dg3TLE').capitalize()
    decision.ECLI = _parseMeta(tag, 'dg3ECLI')
    decision.Language = _parseMeta(tag, 'dg3DecisionLang')
    decision.PDFLink = _parseMeta(tag, 'dg3DecisionPDF')
    decision.CitedCases = _parseMeta(tag, 'dg3aDCI')
    decision.Distribution = _parseMeta(tag, 'dg3DecisionDistributionKey')
    decision.Opponents = _parseMeta(tag, 'dg3Opponent').strip(string.punctuation + string.whitespace)

    ddate = _parseMeta(tag, 'dg3DecisionDate')
    odate = _parseMeta(tag, 'dg3DecisionOnline')
    decision.DecisionDate = datetime.datetime.strptime(ddate, '%d.%m.%Y')
    decision.DecisionOnline = datetime.datetime.strptime(odate, '%d.%m.%Y')    
    
    hw = _parseMeta(tag, 'DC.title')
    finder = re.compile(r'\((.*)\)')
    found = re.search(finder, hw)
    if found:
        decision.Headword = found.group(1)

    decision.Link = tag.u.string


    return decision
#endregion




#region --- methods for retrieval ---   
def GetCaseFromNumber(caseNumber:str):        
    
    def _parseMeta(soup, name):
        v = soup.find('mt', {'n':name})['v']
        return v


    response = Search_Response(partial = "dg3CSNCase:" + caseNumber)
    if not response.reason == "OK":
        return None       


    soup = BeautifulSoup(response.text, "html.parser")
    v = soup.find_all("mt")

    #Get proceedings language
    proceedingsLanguage = _parseMeta(soup, 'dg3DecisionPRL')

    #Find a result that has the decision in this language
    theResult = None
    results = soup.find_all("r")
    for res in results:
        decisionLanguage = _parseMeta(res, 'dg3DecisionLang')
        if decisionLanguage == proceedingsLanguage:
            theResult = res
            break

    if not theResult:
        theResult = results[0]  # no decision in the language of proceedings? Then take whatever is first

    decision = CaseMetaToDecision(theResult)

    return decision


def GetText(decision):

    from app.AppConstants import noPunctionTranslationTable, factFinder, reasonsFinder, orderFinder
    from app.models import Decision

    assert isinstance(decision, Decision)
    if decision.Link == "":
        return        

    #region methods    
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

    def _setText(response):        
        soup = BeautifulSoup(response.content)

        textSection = soup.find(text=factFinder[decision.Language]).findPrevious('p').parent
        textParagraphs = textSection.find_all('p')
        text = "\n\n".join(para.string.strip() for para in textParagraphs if not para.string.translate(noPunctionTranslationTable()).strip() == "")
        split = _splitText(text, decision.Language)
    
        decision.FactsAndSubmissions = split[0]
        decision.Reasons = split[1]
        decision.Order = split[2]
        decision.TextDownloaded = True
        decision.save()
    #endregion

    try:
        response = requests.get(decision.Link)
        _setText(response)

    except Requests.ConnectionError:
        pass

    except RequestsHttpError:
        pass

    except Requests.Timeout:
        pass


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
        "getfields":"*",
        "filter":"0",
        "site":"BoA",
        "client":"BoA_AJAX",
        "ie":"latin1",
        "oe":"latin1",
        "entsp":"0",
        "sort":"date:D:R:d1",
        }

    r = requests.get(searchUrl, params=payload)
    return r
# endregion 
