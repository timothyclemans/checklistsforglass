from django.shortcuts import render
from django.shortcuts import render_to_response
from django.db.models.loading import get_model
from django.http import HttpResponse, HttpResponseRedirect
from models import Checklist, ChecklistV2, ChecklistElement, Device, UnregisteredDevice, Data, AuditTrail
from django.contrib.auth.models import User

import json
from django.template import RequestContext
import traceback
import sys
from django.contrib.auth.decorators import login_required

import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http

try:
    import settings 
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         

        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )

        return response

class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        print exception # or log, or whatever.

        # print traceback
        print '\n'.join(traceback.format_exception(*sys.exc_info()))

def home(request):
    if request.user.is_authenticated():
        context = {'user': request.user, 'checklists_user_created': Checklist.objects.filter(author=request.user), 'checklists_user_createdV2': ChecklistV2.objects.filter(author=request.user)}
    else: 
        context = {}
    return render_to_response("home.html", context)

def get_full_json(request):
    import re
    the_json = request.POST['json']
    matches = re.findall('{"type":"link","checklist_id":\d+}', the_json)
    for match in matches:
        m = re.search('{"type":"link","checklist_id":(?P<id>\d+)}', match)
        checklist = ChecklistV2.objects.get(id=int(m.group('id')))
        the_json = the_json.replace(match, checklist.json[1:-1])
    return HttpResponse(the_json)
    
def get_full_checklist(request, checklist_id):
    import re
    checklist = ChecklistV2.objects.get(id=checklist_id)
    the_json = checklist.json
    matches = re.findall('{"type":"link","checklist_id":\d+}', the_json)
    for match in matches:
        m = re.search('{"type":"link","checklist_id":(?P<id>\d+)}', match)
        checklist = ChecklistV2.objects.get(id=int(m.group('id')))
        the_json = the_json.replace(match, checklist.json[1:-1])
    the_json = the_json.replace("null", "")
    
    the_json = the_json.replace("[,", "[")
    the_json = the_json.replace(",]", "]")
    the_json = the_json.replace(",,", ",")
    return HttpResponse(the_json, content_type="application/json")

#@login_required
def audit_trail(request, data_id):
    data = json.loads(Data.objects.get(id=data_id).data)
    
    context = RequestContext(request, {'data': data})
    return render_to_response('audit_trail.html', context)

def audit_trails(request):
    audit_trails = AuditTrail.objects.filter(user=request.user)
    
    context = RequestContext(request, {'audit_trails': audit_trails})
    return render_to_response('audit_trails.html', context)    

@login_required
def edit_checklist(request, checklist_id):
    if request.POST:
        print request.FILES
        print request.POST
        checklist = Checklist.objects.get(id=checklist_id)
        checklist.name = request.POST['name']
        checklist.delete_elements()
        matches = {}
        
        if 'mass' in request.POST:
            print request.POST['mass']
            for i, item in enumerate(request.POST['mass'].split('\n')):
                print i, item
                checklist_element = ChecklistElement(checklist=checklist, text=item.strip(), order=i)
                checklist_element.save()
                
        else:
            for i, element in enumerate(sorted([j for j in request.POST.keys() if j.startswith('text_')])):
                checklist_element = ChecklistElement(checklist=checklist, text=request.POST[element], order=i)
                checklist_element.save()
                matches[element[5:]] = checklist_element.id
            print checklist.name
            for i in request.FILES:
                f = request.FILES[i]
                ext = f.name[f.name.index('.')+1:]
                checklist_element = ChecklistElement.objects.get(id=matches[i[6:]])
                checklist_element.image = f
                checklist_element.save()
                #with open('/home/tim/checklistsforglass/checklist_images/%s.%s' % (matches[i[6:]], ext), 'wb+') as destination:
                #    for chunk in f.chunks():
                #        destination.write(chunk)
            checklist.save()
    context = RequestContext(request, {'checklist': Checklist.objects.get(id=checklist_id)})
    return render_to_response("edit_checklist.html", context)

def save_image(request, checklist_id):
    if request.POST:
        print request.FILES;
        f = request.FILES['file'];
        file_name = request.POST['file_name']
        file_name = file_name.lower()
        file_name.replace(' ', '_')
        imagef = open('/home/tim/checklistsforglass/media/images/%s_%s.jpg' % (checklist_id, file_name), 'w');
        imagef.write(f.read())
        imagef.close()
        return HttpResponseRedirect('/edit_checklistV2/%s/' % (checklist_id))
    else:
        context = RequestContext(request, {})
        return render_to_response('save_image.html', context)

#@login_required
def edit_checklistV2(request, checklist_id):
    if request.POST:
        
        print request.FILES
        print request.POST
        checklist = ChecklistV2.objects.get(id=checklist_id)
        if (request.user != checklist.author):
            return HttpResponse('not the author')
        checklist.name = request.POST['name']
        checklist.json = request.POST['json']
        matches = {}
        checklist.save()
    if request.user.is_authenticated(): 
        from os import listdir
        from os.path import isfile, join
        images = [ f for f in listdir('/home/tim/checklistsforglass/media/images/') if isfile(join('/home/tim/checklistsforglass/media/images/',f)) if f.startswith(str(checklist_id)) ]   
        context = RequestContext(request, {'checklist': ChecklistV2.objects.get(id=checklist_id), 'page': 'V2', 'checklists': ChecklistV2.objects.filter(author=request.user), 'images': images})
    else:
        context = RequestContext(request, {'checklist': ChecklistV2.objects.get(id=checklist_id), 'page': 'V2', 'checklists': ChecklistV2.objects.all(),})
    return render_to_response("edit_checklistV2.html", context)

@login_required
def create_checklistV2(request):
    
    print 'Create checklist V2: '+str(request.POST)
    if request.POST:
        print request.FILES
        print request.POST
        checklist = ChecklistV2(name=request.POST['name'], author=request.user, json=request.POST['json'])
        checklist.save()
        return HttpResponse(str(checklist.id))
    context = RequestContext(request, {'action': 'create', 'page': 'V2', 'checklists': ChecklistV2.objects.filter(author=request.user),})
    
    return render_to_response("edit_checklistV2.html", context)

@login_required
def create_checklist(request):
    if request.POST:
        print request.FILES
        print request.POST
        checklist = Checklist(name=request.POST['name'], author=request.user)
        checklist.save()

        if 'mass' in request.POST:
            print request.POST['mass']
            for i, item in enumerate(request.POST['mass'].split('\n')):
                print i, item
                checklist_element = ChecklistElement(checklist=checklist, text=item.strip(), order=i)
                checklist_element.save()
        else:
            matches = {}
            for i, element in enumerate(sorted([j for j in request.POST.keys() if j.startswith('text_')])):
                checklist_element = ChecklistElement(checklist=checklist, text=request.POST[element], order=i)
                checklist_element.save()
                matches[element[5:]] = checklist_element.id
            print checklist.name
            for i in request.FILES:
                f = request.FILES[i]
                ext = f.name[f.name.index('.')+1:]
                checklist_element = ChecklistElement.objects.get(id=matches[i[6:]])
                checklist_element.image = f
                checklist_element.save()
            checklist.save()
        for device in Device.objects.filter(user=request.user):
            device.checklists.add(checklist)

    context = RequestContext(request, {'action': 'create'})
    
    return render_to_response("edit_checklist.html", context)

@login_required
def delete_checklist(request, checklist_id):
    checklist = Checklist.objects.get(id=checklist_id)
    checklist.delete()
    return HttpResponse('')

@login_required
def delete_checklistV2(request, checklist_id):
    checklist = ChecklistV2.objects.get(id=checklist_id)
    checklist.delete()
    return HttpResponse('')

def is_registered(request, serial_number):
    answer = serial_number in [i.serial_number for i in Device.objects.all()]
    if answer == False and not serial_number in [i.serial_number for i in UnregisteredDevice.objects.all()]:
        unregistered_device = UnregisteredDevice(serial_number=serial_number)
        unregistered_device.save()
    return HttpResponse(answer)

@login_required
def install(request):
    context = {}
    return render_to_response("install.html", context)

def unregistered_devices(request):
    devices = json.dumps([i.serial_number for i in UnregisteredDevice.objects.all()])
    return HttpResponse(devices, content_type="application/json")

def register_device(request, serial_number):
    device = Device(serial_number=serial_number, user=request.user)
    device.save()
    unregistered_device = UnregisteredDevice.objects.get(serial_number=serial_number)
    unregistered_device.delete()
    return HttpResponse('')

def get_users_checklists(request, user_id):
    checklists = {}
    for checklist in ChecklistV2.objects.filter(author__id=user_id):
        checklists[checklist.name] = checklist.id
    devices = json.dumps(checklists)
    return HttpResponse(devices, content_type="application/json") 
    
def get_all_checklists(request):
    checklists = {}
    for checklist in ChecklistV2.objects.all():
        checklists[checklist.name] = checklist.id
    devices = json.dumps(checklists)
    return HttpResponse(devices, content_type="application/json") 
    
def get_checklists(request, serial_number):
    device = Device.objects.get(serial_number=serial_number)
    device.checklists.all()
    devices = json.dumps([{'name': i.name, 'elements': i.get_elements()} for i in device.checklists.all()])
    return HttpResponse(devices, content_type="application/json") 

def export(request):
    checklists = ChecklistV2.objects.filter(author=request.user)
    cl = []
    for checklist in checklists:
        d = {}
        d['name'] = checklist.name
        d['description'] = checklist.description
        d['video_url'] = checklist.video_url
        d['json'] = checklist.json
        cl.append(d)
    return HttpResponse(json.dumps(cl), content_type="application/json")

def save_data(request):
     
    data = Data(data=request.POST['data'])
    data.save()
    i = 0;
    print len(json.loads(data.data))
    new_data = []
    for item in json.loads(data.data):
        print item
        if item['type'] == 'take_photo':
            import os
            os.system('echo "%s" > /home/tim/checklistsforglass/media/images/temp' % (item['photo']))
            os.system('base64 -d /home/tim/checklistsforglass/media/images/temp > /home/tim/checklistsforglass/media/images/%s_%s.png' % (data.id, i))
            
            item['photo'] = '%s_%s.png' % (data.id, i)
            i += 1
        new_data.append(item)
    data.data = json.dumps(new_data)
    data.save()    
    if 'user_id' in request.POST:
        audit_trail = AuditTrail(data=data, user=User.objects.get(id=request.POST['user_id']), checklist=ChecklistV2.objects.get(id=request.POST['checklist_id']))
        audit_trail.save()
    return HttpResponse('saved')

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from social_auth.exceptions import AuthFailed
from social_auth.views import complete
 
 
  
class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        try:
            return complete(request, backend, *args, **kwargs)
        except AuthFailed:
            messages.error(request, "Your Google Apps domain isn't authorized for this app")
            return HttpResponseRedirect(reverse('home'))
 
 
class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)   
