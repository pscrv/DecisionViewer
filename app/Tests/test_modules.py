"""
Unit tests for modules in app
"""
import datetime
import django
from django.test import TestCase


class oldtest_modules(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_modules, cls).setUpClass()
        django.setup()
        
    def oldtest_epoFacade_SearchByDate(self):
        """Tests the SearchByDate method in epoFacade"""

        from .epofacade import SearchByDate

        response = SearchByDate(datetime.date(2000, 1, 1), datetime.date(2000, 1, 2), 1)
        assert response == ["T 0597/97"]
        
        response = SearchByDate(datetime.date(2001, 10, 1), datetime.date(2001, 10, 5), 1)
        assert response == ["T 0610/98"]
        
        response = SearchByDate(datetime.date(2010, 12, 1), datetime.date(2010, 12, 31))
        assert response[:7] == ["T 1854/07", "T 0832/07", "T 1962/08", "T 0189/06", "T 0528/08", "T 0113/10", "T 0568/05" ]

    def oldtest_epoFacade_SearchByBoard(self):
        """Test the SearchByBoard" method in epofacade"""

        from .epofacade import SearchByBoard

        response = SearchByBoard("3.5.01")
        assert len(response) == 1000

    def oldtest_epoFacade_SearchLatest(self):
        """Test the SearchLatest method in epofacade """

        from .epofacade import SearchLatest

        response = SearchLatest()
        assert len(response) == 10

    def oldtest_epoFacade_SaveSingleCase(self):
        """Tests the SaveSingleCase method of epofacade."""

        from .epofacade import SaveSingleCase
        from .models import Decision
        import django
        
        # assumes T 2273/11 is already in the db
        response = SaveSingleCase("T 2273/11")
        self.assertFalse(response)

        # should always pass, because this is not a case number
        response = SaveSingleCase("NoSuchNumber")
        self.assertFalse(response)

        # should pass when T 0641/00 is no in the db
        response = SaveSingleCase("T 0641/00")
        Decision.objects.filter(CaseNumber = "T 0641/00").delete()
        self.assertTrue(response)

    def oldtest_epoFacade_Search_Response(self):
        """Tests the Search_response method of epoFacade"""

        from .epofacade import Search_Response

        response = Search_Response(partial="dg3CSNCase:T 0641/00")
        self.assertTrue(response.ok)

    def oldtest_epoFacade_GetCaseFromNumber(self):        
        """Tests the GetCaseFromNumber method of epoFacade"""
        
        from .epofacade import GetCaseFromNumber

        response = GetCaseFromNumber("T 2054/12")
        assert(response.CaseNumber == "T 2054/12")





