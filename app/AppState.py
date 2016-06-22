import datetime
from .ClassProperty import ClassProperty
from .epofacade import SearchLatest, GetCaseFromNumber
from .models import Decision

class AppState(object):
    """class to hold app state"""

    _latestDecisions = []
    _latestCaseList = []
    _lastGetLatest = datetime.date.min

    @classmethod
    def __update_latest__(cls, forceUpdate:bool = True):

        if not forceUpdate and cls._lastGetLatest == datetime.date.today():
            return
                
        cls._latestCaseList =  SearchLatest()
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













