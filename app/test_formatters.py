"""
Unit tests for formatters
"""
import django
from django.test import TestCase

class test_decisionFiller(TestCase):    

    @classmethod
    def setUpClass(cls):    
        super(test_decisionFiller, cls).setUpClass()
        django.setup()    


    def test_formatCaseNumber(self):
        from . import dataFormatters
        test = dataFormatters.formatCaseNumber('T 0641/00')
        self.assertEqual(test, 'T 0641/00')
        test = dataFormatters.formatCaseNumber('t 641/00')
        self.assertEqual(test, 'T 0641/00')
        test = dataFormatters.formatCaseNumber('T 1/988')
        self.assertEqual(test, 'T 0001/988')
        test = dataFormatters.formatCaseNumber('Tt 0641/00')
        self.assertEqual(test, 'Tt 0641/00')
        test = dataFormatters.formatCaseNumber('t641/00')
        self.assertEqual(test, 'T 0641/00')

