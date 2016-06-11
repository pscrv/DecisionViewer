"""
Python module to populate the DB with decisions
from the previous month
"""

import datetime
import requests
import re
from string import punctuation
from bs4 import BeautifulSoup

from app.AppConstants import url, noPunctionTranslationTable, factFinder, reasonsFinder, orderFinder

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Decisions.settings')
import django
django.setup()
from app.models import Decision


def _parseMeta(soup, name):
	return soup.find('meta', {'name':name})['content']


def GetDecisions():
	decisionList = requests.get(url).content
	listSoup = BeautifulSoup(decisionList, "html.parser")
	results = listSoup.find_all('r')

	for res in results:

		resUrl = res.u.string
		resFullData = requests.get(resUrl).content
		decisionSoup = BeautifulSoup(resFullData, "html.parser")

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



	
if __name__ == "__main__":
	GetDecisions()