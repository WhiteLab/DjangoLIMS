from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from hiseqlibraries.models import Libraries
from hiseqlibraries.models import Project
from hiseqlibraries.models import Application
from hiseqlibraries.models import SampleType
from hiseqlibraries.models import QC
from hiseqlibraries.models import Files

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render

from django_tables2   import RequestConfig
from django_tables2 import SingleTableView

from hiseqlibraries.tables  import LibrariesTable
from hiseqlibraries.tables  import LibrariesColumnTable
from hiseqlibraries.tables  import QCColumnTable
from hiseqlibraries.tables  import QCTable
from hiseqlibraries.tables  import SummaryTable

from hiseqlibraries.datagrids import UserDataGrid
import xmlrpclib
import re
from datetime import datetime


from hiseqlibraries.models import Summary
from hiseqlibraries.models import SeqStats,AlignStats
from hiseqlibraries.serializers import SummarySerializer, FilesSerializer
from hiseqlibraries.serializers import SeqStatsSerializer, AlignStatsSerializer
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets
import logging
import django_filters
log = logging.getLogger(__name__)

#filter class
class SummaryFilter(django_filters.FilterSet):
    class Meta:
        model = Summary
        fields = ['BID','runID',] #category', 'in_stock', 'min_price', 'max_price']

class SummaryList(generics.ListCreateAPIView): #,SingleTableView):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    filter_class = SummaryFilter

class SummaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    filter_class = SummaryFilter

class FilesList(generics.ListCreateAPIView): #,SingleTableView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

class FilesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

class SeqStatsList(generics.ListCreateAPIView): #,SingleTableView):
    queryset = SeqStats.objects.all()
    serializer_class = SeqStatsSerializer

class SeqStatsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeqStats.objects.all()
    serializer_class = SeqStatsSerializer


class AlignStatsList(generics.ListCreateAPIView): #,SingleTableView):
    queryset = AlignStats.objects.all()
    serializer_class = AlignStatsSerializer

class AlignStatsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlignStats.objects.all()
    serializer_class = AlignStatsSerializer

def libraries(request):

#   get data from bionimbus database

    count_recentkeys = 50 # number of recent keys to be fetched from Bionimbus database
    server=xmlrpclib.ServerProxy( 'https://bc.bionimbus.org/LIMS/keys/call/xmlrpc' )
   # rows=server.recent_keys(count_recentkeys)

    #get latest bid from limsdb
    latestobj = Libraries.objects.latest('createddate')
    dtobj = latestobj.createddate			
    rows=server.keys_after_date( dtobj)
#    rows=server.keys_after_date(datetime(2012,1,1))

    for r in rows:
	libobj = Libraries(bid=r[0].strip(),customer_firstname=r[1].strip(),customer_lastname=r[2].strip())
	#print r[5].strip()
	libobj.project, created =Project.objects.get_or_create(project_name= r[5].strip())
	# created is True when new record is inserted
	print 'inserted new project in Project table from bionimbus db --' + str(created)
	libobj.application,cr=Application.objects.get_or_create(application_name=r[4].strip())
	#libobj.sampletype = SampleType.objects.get(id=1)
	libobj.sampletype = SampleType.objects.get(id=1)
	ds = str(r[3])
	fmt="%Y%m%dT%H:%M:%S"
	dt = datetime.strptime(ds, fmt)
	libobj.createddate = dt
	libobj.save()  #insert or update records


    table = LibrariesTable(Libraries.objects.all())
    lib = Libraries
    cols = LibrariesTable.base_columns.keys()
    # need a list of dicts
    l=[]	
    for i in xrange(0,len(cols)):
	d = {}
    	d = {'colname':cols[i],'selection':i }
	l.append(d)
    
    tablec = LibrariesColumnTable(l)
    RequestConfig(request).configure(table)
    RequestConfig(request).configure(tablec)

    
    if request.method == "POST":

        selcols = request.POST.getlist("selection")
	print selcols
	for i in xrange(0, len(selcols)):
		table.columns[int(selcols[i])].column.visible=False
#	return render_to_response('libraries.html', RequestContext(request, locals()))


    return render(request, 'libraries.html', {'table': table,'tablec':tablec})

def qc(request):
    qcnew = QC.objects.latest('id')
    table = QCTable(QC.objects.all(),order_by='bid',latestid = qcnew.id)
    RequestConfig(request).configure(table)
    cols = QCTable.base_columns.keys()
    l=[]	
    for i in xrange(0,len(cols)):
	d = {}
    	d = {'colname':cols[i],'selection':i }
	l.append(d)
    
    tablec = QCColumnTable(l)
    RequestConfig(request).configure(tablec)
    
    if request.method == "POST":

	print request.POST
	if 'DeleteColumns' in request.POST:
        	selcols = request.POST.getlist("selection")
	#	print selcols
		for i in xrange(0, len(selcols)):
			table.columns[int(selcols[i])].column.visible=False

	if 'AddVersion' in request.POST:
		print 'addversion'
		print request.POST.items()
		#print table.rows[0]
		#insert row to database
		b = request.POST.get('bid',)
		print b
		tmp = Libraries.objects.get(bid=b)#[0])
		q=QC(bid=tmp)
		q.save()

		# get the id for the newly added row
		qcnew = QC.objects.latest('id')
		print 'newqc id'
		print qcnew.id
		#render_to_response will resubmit the form on refresh - not needed

		print len(table.rows)
	#	print max(table.rows['id']) 
		return HttpResponseRedirect('.')

	if 'SaveVersion' in request.POST:
		print 'saveversionhere'

		print request.POST.items()
		# if 'id' not found, gives default value instead of Key error exception
		idvalue = request.POST.get('id', 100001)
		b = request.POST.get('bid',)

		tmp = Libraries.objects.get(bid=b)#[0])
	
#make a form in tables.py and put save button there or try passing values between forms?
		qcrow = QC(id=idvalue, bid=tmp,	
			qubitconcentration=request.POST.get('qubitconcentration',0),
			#dateofBA=request.POST.get('dateofBA',datetime.now),
			BAchiptype = request.POST.get('BAchiptype','Test'),
			volumeremaining=request.POST.get('volumeremaining',0),
			amountremaining=request.POST.get('amountremaining',0))
		qcrow.save()
    return render(request, 'qc.html', {'table': table,'tablec':tablec})


def index(request):
    return HttpResponse("Test -- index page")


def usergrid(request, template_name='hiseqlibraries/usergrid.html'):
     return UserDataGrid(request).render_to_response(template_name)
#def libraries(request):
 #   return render(request, "libraries.html", {"libraries": Libraries.objects.all()})
