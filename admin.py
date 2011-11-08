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

def enable(modeladmin, request, queryset):
	queryset.update(disabled=0)
enable.short_description = "Enable selected entries."
def disable(modeladmin, request, queryset):
	queryset.update(disabled=1)
disable.short_description = "Disable selected entries."

class BuilderAdmin(admin.ModelAdmin):
	list_display = ('builder_name', 'disabled', 'category')
	list_filter = ['project', 'category']
	inlines = [PropertyBuilderInline]
	actions = [enable, disable] 

class CommandAdmin(admin.ModelAdmin):
	list_display = ('project', 'category', 'sequence', 'name', 'type', 'work_dir', 'command')
	list_filter = ['project']
	fields = ['project', 'category', 'sequence', 'name', 'type', 'work_dir', 'rcs_mode', 'command', 'warnOnFail', 'flunkOnFail', 'alwaysRun', 'timeout', 'description', 'descriptionDone']
	ordering = ['project', 'sequence']
	save_as = True

class HostAdmin(admin.ModelAdmin):
	list_display = ('hostname', 'description')
	list_filter = ['builder__project']
	filter_horizontal = ('builder',)

class PropertySchedulerInline(admin.TabularInline):
	model = Property
	extra = 3
	exclude = ['project', 'builder']

class SchedulerAdmin(admin.ModelAdmin):
	list_display = ('name', 'type', 'disabled')
	list_filter = ['project']
	filter_horizontal = ('builderNames','categories',)
	inlines = [PropertySchedulerInline]
	actions = [enable, disable]

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
