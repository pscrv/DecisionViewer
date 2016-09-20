"""
Definitions of models.
"""

import re
from datetime import datetime
from django.db import models

class DecisionManager(models.Manager):
    def create_or_update(
            self, 
            caseNumber:str, 
            decisionLanguage:str,
            **kwargs):
        """ 
        creates and returns a new decision, with the given CaseNumber and ProcedureLanguage, 
        unless one already exists; fills-in or overwrites the **kwargs fields 
        """

        if caseNumber == "" or not decisionLanguage in ['DE', 'EN', 'FR']:
            return None


        allowed_attributes = {
            'DecisionDate', 
            'DecisionOnline', 
            'Applicant', 
            'Opponents',
            'Appellants',
            'Respondents',
            'ApplicationNumber',
            'IPC',
            'Title',
            'Board',
            'Keywords',
            'Articles',
            'Rules',
            'ECLI',
            'CitedCases',
            'Distribution',
            'Headword',
            'Catchwords',
            'DecisionLanguage',
            'Link',
            'PDFLink',
            'MetaDownloaded',
            'TextDownloaded',
            'HasSplitText',
            'FactsHeader',
            'Facts',
            'ReasonsHeader',
            'Reasons',
            'OrderHeader',
            'Order',
            }


        inDB = self.filter(CaseNumber = caseNumber, DecisionLanguage = decisionLanguage).first()

        if inDB is None:
            decision = Decision(CaseNumber = caseNumber, DecisionLanguage = decisionLanguage)
        else:
            decision = inDB

        decision.update(**kwargs)
        return decision


class Decision(models.Model):
    objects = DecisionManager()

    LANGUAGES = [('DE','DE'), ('EN','EN'), ('FR','FR')]
    DISTRIBUTION_CODES = [('A','A'), ('B','B'), ('C','C'), ('D','D')]
    
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
    ProcedureLanguage = models.CharField(choices = LANGUAGES, max_length = 2, default = "")
    #endregion

    #region the decision
    Board = models.CharField(max_length = 16, default = "")
    Keywords = models.TextField(default = "")
    Articles = models.CharField(max_length = 100, default = "")
    Rules = models.CharField(max_length = 100, default = "")
    ECLI = models.CharField(max_length = 20, default = "")
    CitedCases = models.CharField(max_length = 700, default = "")
    Distribution = models.CharField(choices = DISTRIBUTION_CODES, max_length = 1, default = "")
    Headword = models.CharField(max_length = 100, default = "")
    Catchwords = models.TextField(default = "")
    DecisionLanguage = models.CharField(choices = LANGUAGES, max_length = 2, default = "")
    #endregion

    #region links
    Link = models.URLField(max_length = 100, default = "")
    PDFLink = models.URLField(max_length = 100, default = "")
    #endregion
    #endregion

   
    #region text
    TextDownloaded = models.BooleanField(default = False)
    HasSplitText = models.BooleanField(default = False)
    FactsHeader = models.TextField(default = "")
    Facts = models.TextField(default = "")
    ReasonsHeader = models.TextField(default = "")
    Reasons = models.TextField(default = "")
    OrderHeader = models.TextField(default = "")
    Order= models.TextField(default = "")
    #endregion
    
    
    #region methods
    def __str__(self):
        return self.CaseNumber

    #def save(self):
    #    self.Title = self.Title.capitalize()
    #    super(Decision, self).save()


    def update(self, **kwargs):
        
        allowed_attributes = {
            'DecisionDate', 
            'DecisionOnline', 
            'Applicant', 
            'Opponents',
            'Appellants',
            'Respondents',
            'ApplicationNumber',
            'IPC',
            'Title',
            'Board',
            'Keywords',
            'Articles',
            'Rules',
            'ECLI',
            'CitedCases',
            'Distribution',
            'Headword',
            'Catchwords',
            'ProcedureLanguage',
            'Link',
            'PDFLink',
            'MetaDownloaded',
            'TextDownloaded',
            'HasSplitText',
            'FactsHeader',
            'Facts',
            'ReasonsHeader',
            'Reasons',
            'OrderHeader',
            'Order',
            }

        for attribute, value in kwargs.items():
            assert attribute in allowed_attributes, "Attribute " + attribute + " not allowed."
            if (isinstance(value, str)):
                value = value.strip()
            setattr(self, attribute, value)
        
        self.save()

        #endregion





