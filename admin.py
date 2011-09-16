from bbconfig.models import Project, Builder, Command, Host, Scheduler, Property
from django.contrib import admin

#class PropertyAdmin(admin.ModelAdmin):
#	list_display = ('name', 'value')
#	list_filter = ['project', 'builder', 'scheduler']

class PropertyBuilderInline(admin.TabularInline):
	model = Property
	extra = 3
	exclude = ['project', 'scheduler']

class BuilderAdmin(admin.ModelAdmin):
	list_display = ('builder_name', 'disabled')
	list_filter = ['project']
	inlines = [PropertyBuilderInline]

class CommandAdmin(admin.ModelAdmin):
	list_display = ('project', 'sequence', 'name', 'type', 'work_dir', 'command')
	list_filter = ['project']
	fields = ['project', 'sequence', 'name', 'type', 'work_dir', 'rcs_mode', 'command', 'warnOnFail', 'flunkOnFail', 'alwaysRun', 'timeout', 'description', 'descriptionDone']
	ordering = ['project', 'sequence']
	save_as = True

class HostAdmin(admin.ModelAdmin):
	list_display = ('hostname', 'builder', 'description')
	list_filter = ['builder__project']

class PropertySchedulerInline(admin.TabularInline):
	model = Property
	extra = 3
	exclude = ['project', 'builder']

class SchedulerAdmin(admin.ModelAdmin):
	list_display = ('name', 'type', 'disabled')
	list_filter = ['project']
	inlines = [PropertySchedulerInline]

class PropertyProjectInline(admin.TabularInline):
	model = Property
	extra = 3
	exclude = ['builder', 'scheduler']

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'ldap_group', 'url')
	inlines = [PropertyProjectInline]

#admin.site.register(Property, PropertyAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Scheduler, SchedulerAdmin)
