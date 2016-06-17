"""
Definition of models.
"""

import re
from . import epofacade
from datetime import datetime
from django.db import models

class Decision(models.Model):
    CaseNumber = models.CharField(max_length = 16, default = "")
    Board = models.CharField(max_length = 16, default = "")
    DecisionDate = models.DateField(blank=True, null=True)
    OnlineDate = models.DateField(blank=True, null=True)

    Keywords = models.TextField(default = "")
    Rules = models.TextField(default = "")
    Articles = models.TextField(default = "")
    ApplicationNumber = models.IntegerField(default = 0)
    Applicant = models.CharField(max_length = 50, default = "")
    IPC = models.CharField(max_length = 50, default = "")
    ECLI = models.CharField(max_length = 20, default = "")
    Title = models.TextField(default = "")
    Language = models.CharField(max_length = 2, default = "")
    Link = models.CharField(max_length = 100, default = "")
    PDFLink = models.CharField(max_length = 100, default = "")
    CitedCases = models.TextField(default="")
    Distribution = models.CharField(max_length = 1, default = "D")
    Opponents = models.CharField(max_length = 200, default = "")
    Headword = models.CharField(max_length = 100, default = "")


    TextDownloaded = models.BooleanField(default = False)
    FactsAndSubmissions = models.TextField(default = "")
    Reasons = models.TextField(default = "")
    Order = models.TextField(default = "")



    def ReasonsInParagraphs(self):
        self._downloadText() 
        return self.Reasons.split('\n\n')

    def FactsAndSubmissionsInParagraphs(self):
        self._downloadText() 
        return self.FactsAndSubmissions.split('\n\n')

    def OrderInParagraphs(self):
        self._downloadText() 
        return self.Order.split('\n\n')

    def OpponentsList(self):
        return self.Opponents.split('; ')

    def _downloadText(self):
        if not self.TextDownloaded:
            epofacade.GetText(self)
    
    def __str__(self):
        return self.CaseNumber



