'''Utils page for the users Caprende module.'''

def upload_location(instance, filename):
    '''Define the location in the media directory where and how to store the file.'''
    return "%s/%s" % (instance.user.username, filename)

#University Short Names
CAL = "UC Berkeley"
UCLA = "UCLA"
UCD = "UC Davis"
UCI = "UC Irvine"
UCSC = "UC Santa Cruz"
UCSD = "UC San Diego"
UCSB = "UC Santa Barbara"
UCR = "UC Riverside"
UCM = "UC Merced"
SJSU = "San Jose State University"
HARVARD = "Harvard"
PRINCETON = "Princeton"
COLUMBIA = "Columbia"
CORNELL = "Cornell"
YALE = "Yale"
BROWN = "Brown"
DARTMOUTH = "Dartmouth"
UPENN = "University of Pennsylvania"
DUKE = "Duke"
OTHER_UNI = "Unlisted University"

UNIVERSITY_LIST = (
	   (CAL, "UC Berkeley"),
	   (UCLA, "UCLA"),
	   (UCD, "UC Davis"),
	   (UCI, "UC Irvine"),
	   (UCSC, "UC Santa Cruz"),
	   (UCSD, "UC San Diego"),
	   (UCSB, "UC Santa Barbara"),
	   (UCR, "UC Riverside"),
	   (UCM, "UC Merced"),
	   (SJSU, "San Jose State"),
	   (HARVARD, "Harvard"),
	   (PRINCETON, "Princeton"),
	   (COLUMBIA, "Columbia"),
	   (CORNELL, "Cornell"),
	   (YALE, "Yale"),
	   (BROWN, "Brown"),
	   (DARTMOUTH, "Dartmouth"),
	   (UPENN, "University of Pennsylvania"),
	   (DUKE, "Duke"),
	   (OTHER_UNI, "Unlisted University")
)

#Major Short Names
ARTS = "Arts and Humanities"
BUSINESS = "Accounting, Finance, and Business"
LGS = "Legal Studies"
HEALTH_MEDICINE = "Public Health and Medicine"
IDS = "Multi-/Interdisciplinary Studies"
PSS = "Public and Social Services"
STM = "Science and Math"
ENG = "Engineering"
SS = "Social Science"
TPS = "Trades and Personal Services"
OTHER_MAJOR = "Unlisted Major"

MAJOR_LIST = (
	   (ARTS, "Arts and Humanities"),
	   (BUSINESS, "Accounting, Finance, and Business"),
	   (LGS, "Legal Studies"),
	   (HEALTH_MEDICINE, "Public Health and Medicine"),
	   (IDS, "Multi-/Interdisciplinary Studies"),
	   (PSS, "Public and Social Services"),
	   (STM, "Science and Math"),
	   (ENG, "Engineering"),
	   (SS, "Social Science"),
	   (TPS, "Trades and Personal Services"),
	   (OTHER_MAJOR, "Unlisted Major")
)
