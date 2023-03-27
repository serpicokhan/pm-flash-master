'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neuserShiftbject.OrderId.id)
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

from cmms.models.workorder import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import UserShiftForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
from rest_framework import status

from django.template.loader import get_template
import weasyprint

def generate_pdf(request):
    template = get_template('cmms/usershift/userShiftList2.html')
    html = template.render({'my_var': 'Hello world'})

    # Generate the PDF using WeasyPrint
    pdf_file = weasyprint.HTML(string=html).write_pdf()

    # Return the PDF as a response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="my_pdf.pdf"'
    return response
@permission_required('cmms.view_usershift')
def list_userShift(request,id=None):
    #
    books = UserShift.objects.all()
    return render(request, 'cmms/usershift/userShiftList.html', {'userShift': books,'section':'list_userShift'})


##########################################################

def save_userShift_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = UserShift.objects.all()
            data['html_userShift_list'] = render_to_string('cmms/usershift/partialUserShiftList.html', {
                'userShift': books,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}


    data['html_userShift_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def userShift_delete(request, id):
    comp1 = get_object_or_404(UserShift, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  UserShift.objects.all()
        #Tasks.objects.filter(userShiftId=id).update(userShift=id)
        data['html_userShift_list'] = render_to_string('cmms/usershift/partialUserShiftList.html', {
            'userShift': companies,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'userShift': comp1}
        data['html_userShift_form'] = render_to_string('cmms/usershift/partialUserShiftDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def userShift_create(request):
    if (request.method == 'POST'):
        form = UserShiftForm(request.POST)
        return save_userShift_form(request, form, 'cmms/usershift/partialUserShiftCreate.html')
    else:

        form = UserShiftForm()
        return save_userShift_form(request, form, 'cmms/usershift/partialUserShiftCreate.html')




##########################################################
def userShift_update(request, id):
    company= get_object_or_404(UserShift, id=id)
    template=""
    if (request.method == 'POST'):
        form = UserShiftForm(request.POST, instance=company)
    else:
        form = UserShiftForm(instance=company)


    return save_userShift_form(request, form,"cmms/usershift/partialUserShiftUpdate.html",id)
##########################################################

##########################################################
@api_view(['GET'])
def userShift_collection(request):
    if request.method == 'GET':
        print('main serializer')

        posts = UserShift.objects.all()
        serializer = UserShiftSerializer(posts, many=True)
        # for k in serializer.data:
        #     # k.datecreated=DateJob.getDate2(k.datecreated)
        #     k["datecreated"]= str(jdatetime.datetime.fromgregorian(date=datetime.datetime.strptime(k["datecreated"], "%Y-%m-%d").date()).date()).replace('-','/')
        return Response(serializer.data)
