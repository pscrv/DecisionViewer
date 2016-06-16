"""
Definition of models.
"""

import re
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
    FactsAndSubmissions = models.TextField(default = "")
    Reasons = models.TextField(default = "")
    Order = models.TextField(default = "")



    def ReasonsInParagraphs(self):
        return self.FormatInParagraphs(self.Reasons)

    def FactsAndSubmissionsInParagraphs(self):
        return self.FormatInParagraphs(self.FactsAndSubmissions)

    def OrderInParagraphs(self):
        return self.FormatInParagraphs(self.Order)

    def FormatInParagraphs(self, text):
        return text.split("\n\n")
    
    def __str__(self):
        return self.CaseNumber



