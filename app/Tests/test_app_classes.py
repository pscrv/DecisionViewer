"""
Unit tests for AppClasses 
"""
import datetime
import django
from django.test import TestCase


class oldtest_appclass(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_appclass, cls).setUpClass()
        django.setup()

    def oldtest_AppState(self):
        from .AppState import AppState
        response = AppState.LatestDecisions
        self.assertTrue(len(response) == 10)