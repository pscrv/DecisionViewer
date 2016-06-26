import datetime
from .ClassProperty import ClassProperty
from .models import Decision
from . import epoSearch, epoConverter

#from .epofacade import SearchLatest, GetCaseFromNumber


class AppState(object):
    """class to hold app state"""

    _latestDecisions = []
    _latestCaseList = []
    _lastGetLatest = datetime.date.min
    _lastestFromEPO = False

    @classmethod
    def __update_latest__(cls, forceUpdate:bool = True):

        cls._latestCaseList = Decision.objects.order_by('OnlineDate')[:10]

        if not forceUpdate and cls._lastGetLatest == datetime.date.today():
            return
                


        try:
            response = epoSearch.searchLatest()
            epoLatest = epoConverter.toDecisionList()
            cls._latestFromEPO = True
        except:
            epoLatest = []
            cls._latestFromEPO = False



        if epoLatest:
            cls._latestCaseList =  epoLatest
        cls._lastGetLatest = datetime.date.today()

        cls._latestDecisions = []
        for case in cls._latestCaseList:
            caseDecisionInDB = Decision.objects.filter(CaseNumber = case).first()

            if caseDecisionInDB:
                cls._latestDecisions.append(caseDecisionInDB)
            else:
                newDecision = GetCaseFromNumber(case)
                newDecision.save()
                cls._latestDecisions.append(newDecision)


    @ClassProperty
    @classmethod
    def LatestDecisions(cls):
        cls.__update_latest__(forceUpdate=False)
        return cls._latestDecisions
    
    @ClassProperty
    @classmethod
    def LatestFromEPO(cls):
        return cls._latestFromEPO

    @ClassProperty
    @classmethod
    def DBSize(cls):
        return Decision.objects.count

    @ClassProperty
    @classmethod
    def Date(cls):
        return str(datetime.date.today())
        
    @ClassProperty
    @classmethod
    def Year(cls):
        return str(datetime.date.today().year)



    
    @classmethod
    def Count(cls, type='', withmeta=False, withtext=False):
        if withmeta:
            if withtext:
                return Decision.objects.filter(CaseNumber__startswith=type, MetaDownloaded='True', TextDownloaded='True').count()
            else:
                return Decision.objects.filter(CaseNumber__startswith=type, MetaDownloaded='True').count()
        else:
            if withtext:
                return Decision.objects.filter(CaseNumber__startswith=type, TextDownloaded='True').count()
            else:
                return Decision.objects.filter(CaseNumber__startswith=type).count()


    
   