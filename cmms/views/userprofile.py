from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
import os
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from cmms.models.users import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import SysUserImageForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

class UserProfileImageUploadView(View):
    def get(self, request,id=None):
        # photos_list = SysUser.objects.all()
        return render(self.request, 'cmms/user/empty.html', {})

    def post(self, request,id=None):
        company= get_object_or_404(SysUser, id=id)
        form = SysUserForm(self.request.POST, self.request.FILES, instance=company)
        # form = SysUserImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
