"""
Interface methods for querying EPO databases
"""
import requests
import datetime
import re

SEARCHURL = "http://www.epo.org/footer/search.html"



def searchCaseNumber(caseNumber:str):
    response = search(partial = "dg3CSNCase:" + caseNumber)
    return response



def searchLatest(number = 10):
    assert isinstance(number, int), "parameter number must be an integer, but  has type " + str(type(number)) 
    assert number > 0, "parameter number must be > 0, but number = " + str(number)
    return searchByDate(startDate = datetime.date(1900, 1, 1), endDate = datetime.date.today(), number = number)



def searchByDate(startDate, endDate, number = 1000):
    assert isinstance(startDate, datetime.date), "startDate should be datetime, but was " + str(type(startDate))    
    assert isinstance(endDate, datetime.date), "startDate should be datetime, but was " + str(type(startDate))
    assert startDate <= endDate, "startDate should not be later than endDate"

    queryString = "inmeta:dg3DecisionDate:" + str(startDate) + ".." + str(endDate)   
    
    return search(query=queryString, language="lang_en|lang_de|lang_fr", number=number)



def searchByBoard(board, number = 1000):
    finder = re.compile(r'^(\d)\.(\d)\.(\d{2})$')
    found =  re.match(finder, board)
    assert found, "parameter baord must be of the form 3.5.01"

    requiredString = "dg3BOAnDot:" + found.group(1) + found.group(2) + found.group(3)  
    
    return search(required=requiredString, language="lang_en|lang_de|lang_fr", number=number)



def search(query = "", required = "", partial = "", language = None, start = 0, number = 1000):
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
        
    return requests.get(SEARCHURL, params=payload)


def searchDecisionText(url):
    return requests.get(url)