'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neattendancebject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from cmms.business.DateJob import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings

from cmms.models.workorder import *
from cmms.models.users import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AttendanceForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from cmms.business.UserUtility import *
from django.views.decorators.csrf import csrf_exempt,csrf_protect

@permission_required('cmms.view_attendance')
def list_attendance(request,id=None):
    #
    books = Attendance.objects.all().order_by('-datecreated')
    wos=UserUtility.doPaging(request,books)
    return render(request, 'cmms/attendance/attendanceList.html', {'attendance': wos})


##########################################################

def save_attendance_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Attendance.objects.all().order_by('-datecreated')
            wos=UserUtility.doPaging(request,books)
            data['html_attendance_list'] = render_to_string('cmms/attendance/partialAttendanceList.html', {
                'attendance': wos,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}


    data['html_attendance_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def attendance_delete(request, id):
    comp1 = get_object_or_404(Attendance, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  Attendance.objects.all().order_by('-datecreated')
        wos=UserUtility.doPaging(request,companies)
        #Tasks.objects.filter(attendanceId=id).update(attendance=id)
        data['html_attendance_list'] = render_to_string('cmms/attendance/partialAttendanceList.html', {
            'attendance': wos,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'attendance': comp1}
        data['html_attendance_form'] = render_to_string('cmms/attendance/partialAttendanceDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def attendance_create(request):
    if (request.method == 'POST'):
        form = AttendanceForm(request.POST)
        return save_attendance_form(request, form, 'cmms/attendance/partialAttendanceCreate.html')
    else:

        form = AttendanceForm()
        return save_attendance_form(request, form, 'cmms/attendance/partialAttendanceCreate.html')




##########################################################
def attendance_update(request, id):
    company= get_object_or_404(Attendance, id=id)
    template=""
    if (request.method == 'POST'):
        form = AttendanceForm(request.POST, instance=company)
    else:
        form = AttendanceForm(instance=company)


    return save_attendance_form(request, form,"cmms/attendance/partialAttendanceUpdate.html",id)
##########################################################

##########################################################
def attendance_batch_create(request):
    data=dict()
    group=UserGroup.objects.all()
    data['html_attendance_list'] = render_to_string('cmms/attendance/partialBatchAttendanceCreate.html', {
        'group':group,
        'perms': PermWrapper(request.user)
    })
    return JsonResponse(data)
def attendanceGetUser(request,gid):
    users=[]
    if(gid=='0'):
        users=SysUser.objects.filter(userStatus=True)
    elif(gid=='-1'):
        users=[]
    else:
        users=SysUser.objects.filter(id__in=UserGroups.objects.filter(groupUserGroups__id=gid).values_list('userUserGroups__id',flat=True),userStatus=True)
    data=dict()
    data['html_attendance_list'] = render_to_string('cmms/attendance/partialAttendanceList2.html', {
        'attendance': users,
        'perms': PermWrapper(request.user)
    })

    return JsonResponse(data)


@csrf_exempt
def mass_create(request):
    body_unicode = request.body.decode('utf-8')
    data=dict()
    # print("@@@@@@@@@@@@")
    # print(body_unicode)
    # xyz=json.dumps(body_unicode)
    body = json.loads(body_unicode)
    print(type(body))
    final_dictionary = eval(body)
    print(final_dictionary)
    for element in final_dictionary:
         Attendance.objects.create(name=SysUser.objects.get(id=element['userId']),datecreated=DateJob.getDate2(element['date1']),attendanceTime=element['time1'],Ezafekar=element['ezafetime'])
    data['form_is_valid']=True
    books = Attendance.objects.all().order_by('-datecreated')
    wos=UserUtility.doPaging(request,books)
    data['html_attendance_list'] = render_to_string('cmms/attendance/partialAttendanceList.html', {
        'attendance': wos,
        'perms': PermWrapper(request.user)
    })



    return JsonResponse(data)
