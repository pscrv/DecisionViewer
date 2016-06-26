"""
Unit tests for epoConverter
"""
import datetime
import django
from django.test import TestCase


class test_epoConverter(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_epoConverter, cls).setUpClass()
        django.setup()
    
        
    def test_toCaseList(self):
        from .epoSearch import searchCaseNumber, searchByDate
        from .epoConverter import toCaseList

        response = searchCaseNumber("T 2054/12")
        list = toCaseList(response)
        self.assertEqual(len(list), 1)
        self.assertEqual(list[0], 'T 2054/12')
        
        response = searchByDate(datetime.date(2010, 12, 1), datetime.date(2010, 12, 31))
        list = toCaseList(response)
        self.assertEqual(list[:7], ["T 1854/07", "T 0832/07", "T 1962/08", "T 0189/06", "T 0528/08", "T 0113/10", "T 0568/05" ])


    def test_metaToDecision(self):
        from .epoSearch import searchCaseNumber
        from .epoConverter import metaToDecision

        response = searchCaseNumber('T 0641/00')
        decision = metaToDecision(response)
        self.assertEqual(decision.CaseNumber, 'T 0641/00')
        self.assertTrue('COMVIK' in decision.Applicant)

    def test_textToDecision(self):
        from .epoSearch import searchCaseNumber, searchDecisionText
        from .epoConverter import metaToDecision, textToDecision
        
        response1 = searchCaseNumber('T 0641/00')
        decision = metaToDecision(response1)
        response2 = searchDecisionText(decision.Link)
        decision = textToDecision(response2, decision.CaseNumber, decision.ProcedureLanguage)
        self.assertEqual(decision.CaseNumber, 'T 0641/00')
        self.assertTrue(decision.MetaDownloaded)
        self.assertTrue(decision.TextDownloaded)









