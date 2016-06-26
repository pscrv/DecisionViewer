"""
Interface methods for querying EPO databases
"""
import requests
import re
import datetime
import string
from bs4 import BeautifulSoup, element

# replace these urls by references to app.AppConstants, once their forms been properly worked out
searchUrl = "http://www.epo.org/footer/search.html"
singleDecisionUrl = "http://www.epo.org/law-practice/case-law-appeals/recent/"

languageList = ["DE", "EN", "FR"]
languageSuffixes = {"DE":"d", "EN":"e", "FR":"f"}
    
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


#region --- methods for extracting data ---
def CaseMetaToDecision(tag):
       
    from app.models import Decision  
    
    decision = Decision()
    CopyFromMeta(tag, decision)

    return decision


def CopyFromMeta(tag, decision):
       
    from app.models import Decision
    decision.CaseNumber = _parseMeta(tag, 'dg3CSNCase')

    ddate = _parseMeta(tag, 'dg3DecisionDate')
    odate = _parseMeta(tag, 'dg3DecisionOnline')
    decision.DecisionDate = datetime.datetime.strptime(ddate, '%d.%m.%Y')
    decision.DecisionOnline = datetime.datetime.strptime(odate, '%d.%m.%Y')    
    
    decision.Applicant = _parseMeta(tag, 'dg3Applicant')
    decision.Opponents = _parseMeta(tag, 'dg3Opponent')
    #appellants
    #respondents

    decision.ApplicationNumber = _parseMeta(tag, 'dg3APN')
    decision.IPC = _parseMeta(tag, 'dg3CaseIPC')
    decision.Title = _parseMeta(tag, 'dg3TLE').capitalize()
    decision.ProcedureLanguage = _parseMeta(tag, 'dg3DecisionPRL')

    decision.Board = _parseMeta(tag, 'dg3DecisionBoard')
    decision.Keywords = _parseMeta(tag, 'dg3KEY')
    decision.Articles = _parseMeta(tag, 'dg3ArtRef')
    decision.Rules = _parseMeta(tag, 'dg3RuleRef')
    decision.ECLI = _parseMeta(tag, 'dg3ECLI')
    decision.CitedCases = _parseMeta(tag, 'dg3aDCI')
    decision.Distribution = _parseMeta(tag, 'dg3DecisionDistributionKey')
    #catchwords
    decision.DecisionLanguage = _parseMeta(tag, 'dg3DecisionLang')

    decision.PDFLink = _parseMeta(tag, 'dg3DecisionPDF')
    decision.Link = tag.u.string

    hw = _parseMeta(tag, 'DC.title')
    finder = re.compile(r'\((.*)\)')
    found = re.search(finder, hw)
    if found:
        decision.Headword = found.group(1)
        

    decision.MetaDownloaded = True
    decision.save()
    return decision
#endregion




#region --- methods for retrieval ---   
def GetCaseFromNumber(caseNumber:str):       
    
    from app.models import Decision 

    response = Search_Response(partial = "dg3CSNCase:" + caseNumber)
    if not response.reason == "OK":
        return None       


    soup = BeautifulSoup(response.text, "html.parser")
    v = soup.find_all("mt")
    if not v:
        return None

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



    # If there is already a case with this caseNumber
    # copy the meta to it.
    # If not, make a new one.
    
    decision, created = Decision.objects.get_or_create(CaseNumber = caseNumber.strip())            
    decision = CopyFromMeta(theResult, decision)

    return decision


def GetMeta(decision, caseNumber = ""):
    """
    Fills in metadata from the epo site
    Requires either a caseNumber argument or a value for decision.CaseNumber
    The parameter caseNumber is ignored, if decision.CaseNumber exists
    """

    if not decision.CaseNumber:
        if caseNumber:
            decision.CaseNumber = caseNumber
        else:
            return


    response = Search_Response(partial = "dg3CSNCase:" + decision.CaseNumber)
    if not response.reason == "OK":
        return      


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
         
    CopyFromMeta(theResult, decision)
    decision.MetaDownloaded = True
    decision.save()


def GetText(decision):

    from app.AppConstants import noPunctionTranslationTable, factFinder, reasonsFinder, orderFinder

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
        soup = BeautifulSoup(response.content, "html.parser")

        textSection = soup.find('div', {'id':'body'})
        if not textSection:
            return
        textParagraphs = textSection.find_all('p')
        text = "\n\n".join(para.string.strip() for para in textParagraphs if not para.string.translate(noPunctionTranslationTable()).strip() == "")
        split = _splitText(text, decision.DecisionLanguage)
    
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


# a new attempt at GetText
def GetText_2(decision):

    from app.AppConstants import noPunctionTranslationTable, factFinder, reasonsFinder, orderFinder

    if decision.Link == "":
        return        

    #region methods    
    def _parseMeta(soup, name):
        return soup.find('meta', {'name':name})['content']

    def _parasToString(paraList):        
        #text = "\n\n".join(para.string.strip() for para in paraList if not para.string.translate(noPunctionTranslationTable()).strip() == "")        
        text = "\n\n".join(para.string.strip() for para in paraList if not para.string.strip(string.whitespace + string.punctuation) == "")
        return text
        

    def _setText(response):        
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
            decision.FactsHeader = "See Reasons"
            decision.Facts = ""
            decision.ReasonsHeader = ""
            decision.Reasons = _parasToString(textSection.find_all('p'))
            decision.OrderHeader = "See Reasons"
            decision.Order = ""
            decision.TextDownloaded = True
            decision.HasSplitText = False
            decision.save()
            
        
        def loopToHeader(textList, para):
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


        facts = loopToHeader([], headers[0].parent.nextSibling)
        reasons = loopToHeader([], headers[1].parent.nextSibling)
        order = loopToHeader([], headers[2].parent.nextSibling)

        decision.FactsHeader =  headers[0].string
        decision.Facts = _parasToString(facts)
        decision.ReasonsHeader = headers[1].string
        decision.Reasons = _parasToString(reasons)
        decision.OrderHeader = headers[2].string
        decision.Order = _parasToString(order)
        decision.TextDownloaded = True
        decision.HasSplitText = True
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
# endregion 


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
