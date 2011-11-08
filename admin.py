from bbconfig.models import *
from django.contrib import admin

#class PropertyAdmin(admin.ModelAdmin):
#	list_display = ('name', 'value')
#	list_filter = ['project', 'builder', 'scheduler']

class PropertyBuilderInline(admin.TabularInline):
	model = Property
	extra = 3
	exclude = ['project', 'scheduler']

class CategoryAdmin(admin.ModelAdmin):
	pass

class BuilderAdmin(admin.ModelAdmin):
	list_display = ('builder_name', 'disabled', 'category')
	list_filter = ['project', 'category']
	inlines = [PropertyBuilderInline]

class CommandAdmin(admin.ModelAdmin):
	list_display = ('project', 'category', 'sequence', 'name', 'type', 'work_dir', 'command')
	list_filter = ['project']
	fields = ['project', 'category', 'sequence', 'name', 'type', 'work_dir', 'rcs_mode', 'command', 'warnOnFail', 'flunkOnFail', 'alwaysRun', 'timeout', 'description', 'descriptionDone']
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
	filter_horizontal = ('builderNames','categories',)
	inlines = [PropertySchedulerInline]

class PropertyProjectInline(admin.TabularInline):
	model = Property
	extra = 3
	exclude = ['builder', 'scheduler']

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'ldap_group', 'url')
	inlines = [PropertyProjectInline]

#admin.site.register(Property, PropertyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Scheduler, SchedulerAdmin)
