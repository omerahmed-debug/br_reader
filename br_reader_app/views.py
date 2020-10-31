from django.shortcuts import render
from django.http import HttpResponseRedirect
from br_reader_app.models import Reading
from br_reader_app.capture import Capture
# Create your views here.
def index(request):
    readings = Reading.objects.all().order_by('-read_at')[:48]
    return render(request, 'index.html', {'readings': readings, 'table_label': 'Showing Last 48 Readings'})

def read(request):
    capturer = Capture()
    capturer.read_and_save()
    return HttpResponseRedirect('/')

def history(request):
    readings = Reading.objects.all().order_by('-read_at')
    return render(request, 'index.html', {'readings': readings, 'table_label': 'Showing All History Readings'})
