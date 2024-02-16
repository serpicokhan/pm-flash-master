'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nereportbject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings

from cmms.models.report import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import ReportForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.business.ReportUtility import *
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper


@permission_required('cmms.view_report',login_url='/not_found')
def list_report(request,id=None):
    #
    books = Report.objects.all()
    Cat=Report.Category
    wos=ReportUtility.doPaging(request,books)
    return render(request, 'cmms/reports/main.html', {'reports': wos,'cat':Cat,'section':'list_report'})
##########################################################
def save_report_form(request, form, template_name,id=None):
    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Report.objects.all()
            wos=ReportUtility.doPaging(request,books)
            data['html_report_list'] = render_to_string('cmms/reports/partialReportList.html', {
                'reports': wos
            })
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

    context = {'form': form}


    data['html_report_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def report_delete(request, id):
    comp1 = get_object_or_404(Report, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  Report.objects.all()
        #Tasks.objects.filter(reportId=id).update(report=id)
        data['html_report_list'] = render_to_string('cmms/report/partialReportList.html', {
            'report': companies
        })
    else:
        context = {'report': comp1}
        data['html_report_form'] = render_to_string('cmms/report/partialReportDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def report_create(request):
    if (request.method == 'POST'):
        form = ReportForm(request.POST)
        return save_report_form(request, form, 'cmms/reports/partialReportCreate.html')
    else:

        form = ReportForm()
        return save_report_form(request, form, 'cmms/reports/partialReportCreate.html')




##########################################################
def report_update(request, id):
    company= get_object_or_404(Report, id=id)

    if (request.method == 'POST'):
        form = ReportForm(request.POST, instance=company)
    else:
        form = ReportForm(instance=company)


    return save_report_form(request, form,"cmms/reports/partialReportUpdate.html",id)
##########################################################

##########################################################
def reportSearch(request,str):
    data=dict()
    str=str.replace('empty_','')
    str=str.replace('_',' ')
    books=[]
    # print(str,len(str),'&&&&&&&&&&&')
    if(not str):
        books=Report.objects.all()
        str='empty_'
    else:
        books = Report.objects.filter(Q(reportName__contains=str)|Q(reportDetails__contains=str))
    wos=ReportUtility.doPaging(request,books)
    data['html_report_list'] = render_to_string('cmms/reports/partialReportList.html', {
         'reports': wos,
         'perms': PermWrapper(request.user),
     })
    data['html_report_paginator'] = render_to_string('cmms/reports/partialReportPagination.html', {'reports': wos,'pageType':'reportSearch' ,'pageArg':str })
    return JsonResponse(data)
def FilterReportCategory(request,id):
    data=dict()

    books=[]

    if(id=='-1'):
        books = Report.objects.all()
    else:
         books = Report.objects.filter(reportCategory=id)
    wos=ReportUtility.doPaging(request,books)
    data['html_report_list'] = render_to_string('cmms/reports/partialReportList.html', {
         'reports': wos
     })
    # print(wos)
    data['html_report_paginator'] = render_to_string('cmms/reports/partialReportPagination.html', {'reports': wos,'pageType':'FilterReportCategory','pageArg':id})
    return JsonResponse(data)
def make_favorits_report(request,id):
    rep=Report.objects.get(id=id)
    rep.reportFav=not rep.reportFav
    rep.save()
    data=dict()
    data["form_is_valid"]=True
    return JsonResponse(data)
def show_fav_reports(request,id):
    data=dict()

    books=[]

    if(id=='1'):
        books = Report.objects.filter(reportFav=True)
    else:
         books = Report.objects.all()
    wos=ReportUtility.doPaging(request,books)
    data['html_report_list'] = render_to_string('cmms/reports/partialReportList.html', {
         'reports': wos
     })
    # print(wos)
    data['html_report_paginator'] = render_to_string('cmms/reports/rep_pagination2.html', {'reports': wos})
    return JsonResponse(data)
