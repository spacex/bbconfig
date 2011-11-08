from django.db import models

# Create your models here.

class Project(models.Model):
	RCS_TYPE = (
		('S', 'SVN'),
	)
	name = models.CharField('Project identifier', max_length=20)
	description = models.CharField(max_length=200, blank=True)
	rcs_type = models.CharField(max_length=1, choices=RCS_TYPE, default='S')
	rcs_path = models.CharField(max_length=200)
	ldap_group = models.CharField(max_length=20)
	url = models.URLField()
	slaveport = models.PositiveIntegerField()
	statusport = models.PositiveIntegerField()
	tryport = models.PositiveIntegerField()
	#builderNames = models.ManyToManyField(Builder, blank=True)

	def __unicode__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "categories"

class Builder(models.Model):
	project = models.ForeignKey(Project)
	builder_name = models.CharField(max_length=50)
	category = models.ForeignKey(Category, null=True, blank=True)
	disabled = models.BooleanField(default=False)
	makeparams = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.builder_name + ' (' + self.project.name + ')'

class Command(models.Model):
	TYPE_CHOICES = (
		('S', 'Shell'),
		('R', 'RCS Checkout'),
		('C', 'Compile'),
		('T', 'Test'),
		('G', 'Trigger'),
	)
	RCS_MODE = (
		('C', 'Clobber'),
		('U', 'Update'),
	)
	project = models.ForeignKey(Project)
	category = models.ForeignKey(Category, null=True, blank=True)
	name = models.CharField(max_length=50, blank=True)
	description = models.CharField(max_length=50, blank=True)
	descriptionDone = models.CharField(max_length=50, blank=True)
	sequence = models.PositiveIntegerField()
	type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='S')
	work_dir = models.CharField(max_length=200, blank=True)
	#R
	rcs_mode = models.CharField(max_length=1, choices=RCS_MODE, default='C')
	rcs_url = models.CharField(max_length=200, blank=True)
	#SCT
	command = models.TextField(blank=True)
	#S
	warnOnFail = models.BooleanField(default=True)
	#S
	flunkOnFail = models.BooleanField(default=True)
	#S
	alwaysRun = models.BooleanField(default=False)
	#T
	timeout = models.PositiveIntegerField(default=0)
	#G
	#schedulerNames = models.ManyToManyField(Scheduler)

	def __unicode__(self):
		return self.project.name + " (" + self.category.name + ")-" + str(self.sequence)

	class Meta:
		ordering = ['project', 'sequence']

class Host(models.Model):
	builder = models.ManyToManyField(Builder, blank=True)
	#builder = models.ManyToManyField(Builder)
	hostname = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	max_builds = models.PositiveIntegerField()
	description = models.CharField(max_length=50, blank=True)

	class Meta:
		ordering = ['builder__project']

class Scheduler(models.Model):
	SCHEDULER_CHOICES = (
		('S', 'SingleBranchScheduler'),
		('A', 'AnyBranchScheduler'),
		('D', 'Dependent'),
		('P', 'Periodic'),
		('N', 'Nightly'),
		('J', 'Try (Jobdir)'),
		('U', 'Try (UserPass)'),
		('R', 'Triggerable'),
	)
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=50, blank=True)
	type = models.CharField(max_length=1, choices=SCHEDULER_CHOICES, default='S')
	disabled = models.BooleanField(default=False)
	categories = models.ManyToManyField(Category, blank=True)
	builderNames = models.ManyToManyField(Builder, blank=True)#, limit_choices_to = {'project': project} )

	#SAN - branch
	branch = models.CharField(max_length=100, null=True, blank=True)
	#SA - treeStableTimer
	treeStableTimer = models.PositiveIntegerField(null=True, blank=True)
	#SA - fileIsImportant(func), change_filter, N if onlyIfChanged
	#D - models.ForeignKey(Scheduler, null=True)
	dependent_upstream = models.ForeignKey('self', null=True, blank=True)
	#P - periodicBuildTimer
	periodic_periodicBuildTimer = models.PositiveIntegerField(null=True, blank=True)
	#N - minute, hour, dayOfMonth, month, dayOfWeek
	nightly_minute = models.PositiveIntegerField(null=True, blank=True)
	nightly_hour = models.PositiveIntegerField(null=True, blank=True)
	nightly_dayOfMonth = models.PositiveIntegerField(null=True, blank=True)
	nightly_month = models.PositiveIntegerField(null=True, blank=True)
	nightly_dayOfWeek = models.PositiveIntegerField(null=True, blank=True)
	#J - jobdir
	try_jobdir = models.CharField(max_length=255, null=True, blank=True)
	#U - userpass, port
	try_port = models.PositiveIntegerField(null=True, blank=True)
	try_user = models.CharField(max_length=50, null=True, blank=True)
	try_password = models.CharField(max_length=50, null=True, blank=True)

class Property(models.Model):
	project = models.ForeignKey(Project, null=True, blank=True)
	builder = models.ForeignKey(Builder, null=True, blank=True)
	scheduler = models.ForeignKey(Scheduler, null=True, blank=True)
	name = models.CharField(max_length=50)
	value = models.CharField(max_length=300)

	class Meta:
		verbose_name_plural = "properties"
