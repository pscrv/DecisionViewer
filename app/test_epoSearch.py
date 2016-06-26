"""
Unit tests for epoSearch
"""
import datetime
import django
from django.test import TestCase


class test_epoSearch(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_epoSearch, cls).setUpClass()
        django.setup()
        
    
    def test_searchByDate(self):
        """Tests the searchByDate method"""

        from .epoSearch import searchByDate

        response = searchByDate(datetime.date(2000, 1, 1), datetime.date(2000, 1, 2), 1)
        self.assertIn('T 0597/97', response.text)
        
        response = searchByDate(datetime.date(2001, 10, 1), datetime.date(2001, 10, 5), 1)
        self.assertIn("T 0610/98", response.text)
        
        response = searchByDate(datetime.date(2010, 12, 1), datetime.date(2010, 12, 31))
        self.assertIn("T 1854/07", response.text)
        self.assertIn("T 1962/08", response.text)


    def test_searchByBoard(self):

        from .epoSearch import searchByBoard

        response = searchByBoard("3.5.01")
        self.assertIn('T 0641/00', response.text)

        
    def test_searchCaseNumber(self):        
        
        from .epoSearch import searchCaseNumber

        response = searchCaseNumber("T 2054/12")
        self.assertIn("T 2054/12", response.text)