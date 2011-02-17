# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from familytree.models import *
from familytree.helper import *

#created this as a test
class theFamily():
	#fast objects
	familyDir = Person.objects.all()
	males  = familyDir.filter(sex='M')
	females = familyDir.filter(sex='F')

	#Names info
	firstname_distinct = familyDir.values('firstname').distinct()
	surname_distinct = familyDir.values('surname').distinct()        
	middlename1_distinct = familyDir.values('middlename1').distinct()    
	middlename2_distinct = familyDir.values('middlename2').distinct() 

	firstname_reuse = name_count(familyDir.values('firstname'))
	surname_reuse = name_count(familyDir.values('surname'))
	middlename_reuse = name_count(familyDir.values('middlename1') + familyDir.values('middlename2')))
	all_reuse = name_count(familyDir.values('firstname') + familyDir.values('middlename1') + familyDir.values('middlename2'))

def index(request):
        people = Person.objects.all().order_by('-created_date')[:5]
	about = theFamily
        return render_to_response('familytree/index.html', {'people': people, 'about': about})

