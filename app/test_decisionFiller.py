"""
Unit tests for decisionFiller
"""
import datetime
import django
from django.test import TestCase


class test_decisionFiller(TestCase):
    

    @classmethod
    def setUpClass(cls):    
        super(test_decisionFiller, cls).setUpClass()
        django.setup()
    

    def test_getMeta(self):
        from . import decisionFiller
        decision = decisionFiller.get_meta('T 0641/00', 'EN', forceDownload = True)
        self.assertEqual(decision.CaseNumber, 'T 0641/00')
        self.assertTrue(decision.MetaDownloaded)


    def test_getText(self):
        from . import decisionFiller
        decision = decisionFiller.get_text('T 0641/00', 'EN', forceDownload = True)
        self.assertEqual(decision.CaseNumber, 'T 0641/00')
        self.assertTrue(decision.MetaDownloaded)
        self.assertTrue(decision.TextDownloaded)
