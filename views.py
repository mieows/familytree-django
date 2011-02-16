# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from familytree.models import *
# Create your views here.
def index(request):
        people = Person.objects.all().order_by('-created_date')[:5]

        return render_to_response('familytree/index.html', {'people': people})

