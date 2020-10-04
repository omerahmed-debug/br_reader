from django.shortcuts import render
from django.http import HttpResponse
from capture import Capture

# Create your views here.
def index(request):
    return render(request, 'index.html')

def read(request):
 #   task()
    val = 2
    return HttpResponse("Barometer Reading: %s" % val)
