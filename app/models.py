"""
Definition of models.
"""

import re
from . import epofacade
from datetime import datetime
from django.db import models

class Decision(models.Model):
    CaseNumber = models.CharField(max_length = 16, default = "")

    #region metadata
    MetaDownloaded = models.BooleanField(default = False)

    #region dates
    DecisionDate = models.DateField(blank=True, null=True)
    OnlineDate = models.DateField(blank=True, null=True)
    #endregion

    #region parties
    Applicant = models.CharField(max_length = 50, default = "")
    Opponents = models.CharField(max_length = 200, default = "")
    Appellants = models.CharField(max_length = 200, default = "")
    Respondents = models.CharField(max_length = 200, default = "")
    #endregion

    #region application
    ApplicationNumber = models.CharField(max_length = 15, default = "")
    IPC = models.CharField(max_length = 50, default = "")
    Title = models.TextField(default = "")
    ProcedureLanguage = models.CharField(max_length = 2, default = "")
    #endregion

    #region the decision
    Board = models.CharField(max_length = 16, default = "")
    Keywords = models.TextField(default = "")
    Articles = models.CharField(max_length = 100, default = "")
    Rules = models.CharField(max_length = 100, default = "")
    ECLI = models.CharField(max_length = 20, default = "")
    CitedCases = models.CharField(max_length = 700, default = "")
    Distribution = models.CharField(max_length = 1, default = "D")
    Headword = models.CharField(max_length = 100, default = "")
    Catchwords = models.TextField(default = "")
    DecisionLanguage = models.CharField(max_length = 2, default = "")
    #endregion

    #region links
    Link = models.CharField(max_length = 100, default = "")
    PDFLink = models.CharField(max_length = 100, default = "")
    #endregion
    #endregion

   
    #region text
    TextDownloaded = models.BooleanField(default = False)
    HasSplitText = models.BooleanField(default = False)
    FactsAndSubmissions = models.TextField(default = "")
    Reasons = models.TextField(default = "")
    Order= models.TextField(default = "")
    #endregion
    


    def FactsAndSubmissionsInParagraphs(self):
        return self.FactsAndSubmissions.split('\n\n')

    def ReasonsInParagraphs(self):
        return self.Reasons.split('\n\n')

    def OrderInParagraphs(self):
        return self.Order.split('\n\n')

    def OpponentsList(self):
        return self.Opponents.split('; ')

    def CitedCases_List(self):
        if self.CitedCases == "":
            return []
        else:
            return self.CitedCases.split(',')

    def FillData(self, forcedownload = False):
        if forcedownload or not self.MetaDownloaded:
            epofacade.GetMeta(self)
        if forcedownload or not self.TextDownloaded:
            epofacade.GetText_2(self)

    
    def __str__(self):
        return self.CaseNumber



