from django.shortcuts import render, get_object_or_404

from bbconfig.models import *

def index(request):
	return render(request, 'index.html')

def project_byid(request, project_id):
	project = get_object_or_404(Project.objects.filter(id=project_id))

	return project_render(request, project)

def project_byname(request, name):
	project = get_object_or_404(Project.objects.filter(name=name))

	return project_render(request, project)

def project_render(request, project):
	ordered_commands = project.command_set.order_by('category', 'sequence')

	dic = {}
	dic['project'] = project
	dic['ordered_commands'] = ordered_commands

	return render(request, 'project_summary.html', dic)
