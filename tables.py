import django_tables2 as tables
from django_tables2 import A
from hiseqlibraries.models import Libraries
from hiseqlibraries.models import Summary
from hiseqlibraries.models import QC
from django.utils.safestring import mark_safe
from django.utils.html import escape 
#from hiseqlibraries.models import LibrariesColumn

class SummaryTable(tables.Table):
    class Meta:
        model = Summary
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}


class LibrariesTable(tables.Table):
    class Meta:
        model = Libraries
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}

class QCTable(tables.Table):
    #addversion = tables.LinkColumn('/hiseqlibraries/index', args=[A('pk')])
    fn = tables.Column(accessor='bid.customer_firstname')
    ln = tables.Column(accessor='bid.customer_lastname')
    st = tables.Column(accessor='bid.sampletype')
    id = tables.Column() 
    #editable = tables.LinkColumn('edit_form',verbose_name='edit') 
    addversion = tables.TemplateColumn(verbose_name=('Add Version'),
                                    template_name='hiseqlibraries/templates/addversion.html',
                                    sortable=False)
    TEMPLATE = '''
   <a href="{% url index record.pk %}" class="tbl_icon edit">Edit</a>
   <a href="{% url index record.pk %}" class="tbl_icon delete">Delete</a>
'''

    def __init__(self, *args, **kwargs):
        self.latestid = kwargs.pop('latestid', None)
	super(QCTable, self).__init__(*args, **kwargs)


    def render_qubitconcentration(self,value,record):
	if (record.id == self.latestid):
		#return mark_safe('''<form action="" method="post">
		#			"{{% csrf_token %%}}"
	#	context = super(QCTable, self).get_context_data(**kwargs)
	#	csrf_token = context.get('csrf_token', None)
		return mark_safe('''<form action="" method="post">
					<input type='text' value=%s>
					''' %(value ))
	else:
		return str(value)
    
    def render_dateofBA(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)
	

    def render_BAchiptype(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)
    
    def render_volumeremaining(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)
    
    def render_amountremaining(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)


    def render_qubitmolarity(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)


    def render_BAsize(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)


    def render_BAconcentration(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)


    def render_BAmolarity(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)

    def render_folddiff(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)


    def render_sourceid(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>''' %(value) )
	else:
		return str(value)

    def render_version(self,value,record):
	if (record.id == self.latestid):
		return mark_safe('''<input type='text' value=%s>
					<input class="btn btn-medium btn-primary" type="submit" value="Save Version" name="SaveVersion" />
					</form>''' %(value) )
	else:
		return str(value)

	
#save current id being rendered
#if current id is latest id, all columns change to 'input' type
    #column_name = tables.TemplateColumn('<a href="{{index}}">{{record.bid}}</a>') 
    class Meta:
        model = QC
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue", "index": "index"}
	sequence = ("id","bid","fn", "ln","st", "...")
class LibrariesColumnTable(tables.Table):
    colname = tables.Column()
    selection = tables.CheckBoxColumn()
    #selection = tables.CheckBoxColumn(attrs={"checked": "checked"})
    class Meta:
  ##      model = Libraries.get_fields()# add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}

class QCColumnTable(tables.Table):
    colname = tables.Column()
    selection = tables.CheckBoxColumn()
    class Meta:
        attrs = {"class": "paleblue"}
