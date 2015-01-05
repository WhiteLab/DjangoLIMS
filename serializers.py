from django.forms import widgets
from rest_framework import serializers
from hiseqlibraries.models import Summary,Files,SeqStats,AlignStats

class SummarySerializer(serializers.ModelSerializer):
	class Meta:
	        model = Summary
        #	fields = ( 'SampleID', 'runID', 'Lane','SampleID', 'SampleRef', 'Index', 'Description', 'Control', 'Project', 'Yield_Mbases', 'percentagePF', 'numReads','percentageRawClustersperlane', 'percentagePerfectIndexReads', 'percentageOneMismatchReads', 'percentageMorethanQ30Bases','MeanQualityScore')

class FilesSerializer(serializers.ModelSerializer):
	class Meta:
	        model = Files

class SeqStatsSerializer(serializers.ModelSerializer):
	class Meta:
	        model = SeqStats

class AlignStatsSerializer(serializers.ModelSerializer):
	class Meta:
	        model = AlignStats

