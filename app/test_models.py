
import django
from django.test import TestCase

class test_models(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_models, cls).setUpClass()
        django.setup()

    def test_Model(self):
        from .models import Decision
        dec = Decision.objects.create_or_update('T 0641/00', 'EN')
        dec = Decision.objects.create_or_update(caseNumber='T 0641/00', decisionLanguage='EN', Applicant = 'Someone', ProcedureLanguage = 'DE')
        dec = Decision.objects.create_or_update('T 0641/00', 'EN', Applicant = 'Someone else', Catchwords = '  Catchword      ')
        dec = Decision.objects.create_or_update('T 0641/00', 'FR', Applicant = "Quelqu'un   ", Title="Je ne SAIS pas cE qui va être cette titre    ")
        self.assertEqual(Decision.objects.filter(CaseNumber='T 0641/00').count(), 2)
        got1 = Decision.objects.get(CaseNumber='T 0641/00', DecisionLanguage = 'EN')
        got2 = Decision.objects.get(CaseNumber='T 0641/00', DecisionLanguage = 'FR')
        self.assertEqual(got1.Applicant, 'Someone else')
        self.assertEqual(got1.Catchwords, 'Catchword')
        self.assertEqual(got2.Title, "Je ne sais pas ce qui va être cette titre")

if __name__ == '__main__':
    unittest.main()
