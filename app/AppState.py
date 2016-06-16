import datetime
from .ClassProperty import ClassProperty
from .epofacade import SearchLatest, GetSingleCase, CaseDataToDecision
from .models import Decision

class AppState(object):
    """class to hold app state"""

    _latestDecisions = []
    _latestCaseList = []
    _lastGetLatest = datetime.date.min

    @classmethod
    def __update__(cls, forceUpdate:bool = True):
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
                newDecision = Decision()
                CaseDataToDecision(caseNumber = case, decision = newDecision)
                cls._latestDecisions.append(newDecision)




    @ClassProperty
    @classmethod
    def LatestDecisions(cls):
        cls.__update__(forceUpdate=False)
        return cls._latestDecisions












