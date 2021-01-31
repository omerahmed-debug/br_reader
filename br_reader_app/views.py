from django.shortcuts import render
from django.http import HttpResponseRedirect
from br_reader_app.models import Reading
from br_reader_app.capture import Capture
from django.utils.timezone import make_aware
from django.conf import settings
import datetime

# Create your views here.
def index(request):
    readings = Reading.objects.all().order_by('-read_at')[:48]
    return render(request, 'index.html', {'readings': readings, 'table_label': 'Showing Last 48 Readings'})

def read(request):
    capturer = Capture()
    capturer.read_and_save()
    return HttpResponseRedirect('/')

def history(request):
    if 'date_picker' in request.GET:
        selectedDate = request.GET['date_picker']
    else:
        selectedDate = datetime.date.today().strftime('%Y-%m-%d')
    st = datetime.datetime.strptime(selectedDate, '%Y-%m-%d')
    ed = datetime.datetime.strptime(selectedDate, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
    st = make_aware(st)
    ed = make_aware(ed)
    formattedDate = st.strftime('%A, %d %b %Y')
    readings = Reading.objects.filter(read_at__range=[st, ed]).order_by('-read_at')
    return render(request, 'index.html', {'readings': readings, 'table_label': f'Showing Readings for {formattedDate}', 'date_picker': selectedDate})
