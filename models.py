from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Project(models.Model):
	project_name = models.CharField(max_length=100)
	def __unicode__(self):  # string to show up in admin interface
        	return self.project_name
class Application(models.Model):
	application_name = models.CharField(max_length=50,default='Not specified')

	def __unicode__(self):  # string to show up in admin interface
		return self.application_name
class SampleType(models.Model):
	sampletype_name = models.CharField(max_length=50,default='Not specified')

	def __unicode__(self):  # string to show up in admin interface
		return self.sampletype_name
class Libraries(models.Model):
	bid = models.CharField(max_length=10,unique=True) # from bionimbus db
	customer_firstname = models.CharField(max_length=200,default='Not specified')
	customer_lastname = models.CharField(max_length=200,default='Not specified')
	project = models.ForeignKey(Project)
	application = models.ForeignKey(Application)	
	sampletype = models.ForeignKey(SampleType,default='Not specified')
	protocol = models.CharField(max_length=200,default='Not specified',blank=True)
	receiveddate = models.DateTimeField('Date sample received',default=datetime.now, blank=True)
	createddate = models.DateTimeField('Date BID created',default=datetime.now, blank=True)
	status_active = models.BooleanField(default = True)

		
	def __unicode__(self):  # string to show up in admin interface
		return  '%s' % (self.bid) #, self.customer_firstname,self.customer_lastname, self.project,self.application, self.receiveddate, self.status_active)
#		return  u'%s %s %s %s %s %s %s' % (self.bid, self.customer_firstname,self.customer_lastname, self.project,self.application, self.receiveddate, self.status_active)

	class Meta:
		verbose_name_plural = "Libraries"


class QC(models.Model):
	bid = models.ForeignKey(Libraries)
#	customer_firstname = models.ForeignKey(Libraries,related_name='Liraries_customer_firstname',default='Not specified')
#	customer_lastname = models.ForeignKey(Libraries,related_name='Liraries_customer_lastname',default='Not specified')
#	sampletype = models.ForeignKey(SampleType,default='Not specified')
	qubitconcentration=models.DecimalField('Qubit Concentration (ng/ul)',max_digits=10, decimal_places=2,default=0)
	dateofBA=models.DateTimeField('Date of BioAnalyzer',default=datetime.now,blank=True)
	BAchiptype = models.CharField(max_length=10,default='Not specified')
	volumeremaining=models.DecimalField('Volume Remaining',max_digits=10, decimal_places=2,default=0)
	amountremaining=models.DecimalField('Amount Remaining',max_digits=10, decimal_places=2,default=0)
	qubitmolarity=models.DecimalField('Qubit Molarity (nmol/L)',max_digits=10, decimal_places=2,default=0)
	BAsize = models.IntegerField('BioAnalyzer size(bp)',default=0)
	BAconcentration=models.DecimalField('BioAnalyzer  Concentration (ng/ul)',max_digits=10, decimal_places=2,default=0)
	BAmolarity=models.DecimalField('BioAnalyzer Molarity (nmol/L)',max_digits=10, decimal_places=2,default=0)
	folddiff=models.DecimalField('Fold Difference (Qubit:BioAnalyzer)',max_digits=10, decimal_places=2,default=0)
	passed=models.BooleanField(default = True)
	sourceid=models.CharField(max_length=11)
	version = models.IntegerField(default=0)
	
	def __unicode__(self):  # string to show up in admin interface
                return  '%s,%s,%s,%s' % (self.bid, self.qubitconcentration, self.passed,  self.sourceid)

class Summary(models.Model):

	Lane =models.CharField(max_length=10)
	BID=models.CharField(max_length=10,default='Not specified')
 	SampleRef=models.CharField(max_length=20,default='Not Specified')
 	Index=models.CharField(max_length=32,default='Not specified')
 	Description=models.CharField(max_length=100,default='Not specified')
 	Control=models.CharField(max_length=10,default='Not specified')
 	Project=models.CharField(max_length=100,default='Not specified')
 	Yield_Mbases=models.CharField(max_length=100,default='Not specified')
 	percentagePF=models.CharField(max_length=10,default='Not specified')
 	numReads=models.CharField(max_length=100,default='Not specified')
 	percentageRawClustersperlane=models.CharField(max_length=10,default='Not specified')
 	percentagePerfectIndexReads=models.CharField(max_length=10,default='Not specified')
 	percentageOneMismatchReads=models.CharField(max_length=10,default='Not specified')
 	percentageMorethanQ30Bases=models.CharField(max_length=10,default='Not specified')
 	MeanQualityScore=models.CharField(max_length=10,default='Not specified')
        runID = models.CharField(max_length=100)


class Files(models.Model):
	
	fileID = models.AutoField(primary_key=True) #auto increment ID
	FILETYPE_CHOICES = [('BAM','.bam'),('FASTQ','.fastq'),('WIG','.wig'),('BED','.bed'),('HIST','.hist')]
	fileType = models.CharField(max_length=10, choices=FILETYPE_CHOICES, default='FASTQ')
	name = models.CharField(max_length=200,default='Not specified')
	md5 = models.CharField(max_length=200,default=0)
	date = models.DateTimeField('Date created',default=datetime.now)

class Location(models.Model):

	fileID = models.ForeignKey(Files)
	location_url = models.CharField(max_length=500,default='')
	date = models.DateTimeField('Date',default=datetime.now)

class Source(models.Model):
	
	fileID = models.ForeignKey(Files)
	sourceRefID = models.IntegerField('ID of file(s) from which this file is created')

class SeqStats(models.Model):

	fileID = models.ForeignKey(Files)
	reads = models.BigIntegerField(validators=[MinValueValidator(0)],default=0)
	bases = models.BigIntegerField(validators=[MinValueValidator(0)],default=0)
	md5 = models.CharField(max_length=200,default=0)

class AlignStats(models.Model):
	
	fileID = models.ForeignKey(Files)
	align_bp = models.BigIntegerField(validators=[MinValueValidator(0)],default=0)
	rmdup_bp = models.BigIntegerField(validators=[MinValueValidator(0)],default=0)
	align_fr = models.FloatField(validators=[MinValueValidator(0.0),
                                      MaxValueValidator(1.0)])
	rmdup_fr = models.FloatField(validators=[MinValueValidator(0.0),
                                      MaxValueValidator(1.0)])
	md5 = models.CharField(max_length=200,default=0)

class HistStats(models.Model):


	fileID = models.ForeignKey(Files)
	target = mmodels.CharField(max_lenghth=200, default='Not specified')
	target_size = models.BigIntegerField(validators=[MinValueValidator(0)],default=0)
	align_bp_ot = models.BigIntegerField(validators=[MinValueValidator(0)],default=0)
	rmdup_bp_ot = models.BigIntegerField(validators=[MinValueValidator(0)],default=0)
	10th = models.DecimalField(max_digits=20, decimal_places=5,default=0)
	25th = models.DecimalField(max_digits=20, decimal_places=5,default=0)
	50th = models.DecimalField(max_digits=20, decimal_places=5,default=0)
	75th = models.DecimalField(max_digits=20, decimal_places=5,default=0)
	90th = models.DecimalField(max_digits=20, decimal_places=5,default=0)
	avg = models.DecimalField(max_digits=20, decimal_places=5,default=0)
	std = models.DecimalField(max_digits=20, decimal_places=5,default=0)


##class LibrariesColumn(models.Model):
#	lib = Libraries
#	def __init__(self):
#		return lib.get_fields()
