
"""
A collection of global constants
"""

from string import punctuation

def noPunctionTranslationTable():
	return str.maketrans({ord(ch):"" for ch in punctuation})	

url = "http://www.epo.org/footer/search.html?site=BoA&entqr=0&q=PDF%2Binmeta:dg3DecisionDate:2016-05-01..2016-06-30&lr=lang_en|lang_fr|lang_de&sort=date:D:S:d1&filter=0&num=1000"
	

factFinder = {
	'DE' : 'Sachverhalt und Anträge',
	'EN': 'Summary of Facts and Submissions',
	'FR': 'Exposé des faits et conclusions',}

reasonsFinder = {
		'DE' : 'Entscheidungsgründe',
		'EN': 'Reasons for the Decision',
		'FR': 'Motifs de la décision',}

orderFinder = {
	'DE' : 'Entscheidungsformel',
	'EN' : 'Order',
	'FR' : 'Dispositif',}




