from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
from cmms.models.workorder import *
from cmms.api.WOSerializer import *
from cmms.business.WOUtility import WOUtility
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # print(request.user)


        content = {'message': 'Hello, World!'}
        return Response(content)

class MiniView(APIView):
    def filterUser(self,request,books):
        if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
            books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))|Q(RequestedUser__userId=request.user)).order_by('-datecreated','-timecreated')
        else:
            books=books.order_by('-datecreated','-timecreated')
        return books
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        # print("!23")
        posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False,visibile=True).order_by('-datecreated')
        # print(request.user)
        companies=self.filterUser(request,posts)
        # wos=WOUtility.doPaging(request,companies)
        wos=companies[:50]
        serializer = WOSerializer2(wos, many=True)
        # for k in serializer.data:
        #     # k.datecreated=DateJob.getDate2(k.datecreated)
        #     k["datecreated"]= str(jdatetime.datetime.fromgregorian(date=datetime.datetime.strptime(k["datecreated"], "%Y-%m-%d").date()).date()).replace('-','/')
        return Response(serializer.data)
class RegMiniView(APIView):
    def filterUser(self,request,books):
        if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
            books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))|Q(RequestedUser__userId=request.user)).order_by('-datecreated','-timecreated')
        else:
            books=books.order_by('-datecreated','-timecreated')
        return books
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        # print("!23")
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        # print(request.user.id,"req")
        rq=SysUser.objects.get(userId=request.user.id)
        # request.data['RequestedUser']=rq.id

        # print('123')
        serializer =MiniWorkorderSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.RequestedUser=SysUser.objects.get(userId=request.user)

            io1=serializer.save()
            io1.RequestedUser=rq

            io1.save()
            WOUtility.create_task_when_wo_created(request,io1.id)
            WOUtility.create_notification(request,io1.id)

            # print("her2!")

            posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False,visibile=True).order_by('-datecreated')
            companies=self.filterUser(request,posts)
            # wos=WOUtility.doPaging(request,companies)
            wos=companies[:50]
            serializer = WOSerializer2(wos, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DetailedMiniView(APIView):

    permission_classes = (IsAuthenticated,)
    def post(self,request):
        # print("!23")
            # print(request.POST)
            id=request.GET.get('id',False)
            # print(id)
            if(id):
                try:
                    posts = WorkOrder.objects.get(id=id,RequestedUser__userId=request.user)
                except WorkOrder.DoesNotExist:
                    content = {'message': 'Nothing to Show'}
                    # print(content)
                    return Response(content)
                # print(posts)
                # print(request.user)
                serializer = WOSerializer2(posts)
                # serializer = WOSerializer(posts)
                # print(serializer)
                return Response(serializer.data)
            else:
                content = {'message': 'Error'}
                # print(content)
                return Response(content)
class DeleteMiniView(APIView):
    def filterUser(self,request,books):
        if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
            books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))|Q(RequestedUser__userId=request.user)).order_by('-datecreated','-timecreated')
        else:
            books=books.order_by('-datecreated','-timecreated')
        return books

    permission_classes = (IsAuthenticated,)
    def post(self,request):
            id=request.GET.get('id',False)
            if(id):
                try:
                    post = WorkOrder.objects.get(id=id,RequestedUser__userId=request.user)
                    post.delete()
                except WorkOrder.DoesNotExist:
                    content = {'message': 'Nothing to Show'}
                    return Response(content)
                posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False,visibile=True).order_by('-datecreated')
                companies=self.filterUser(request,posts)
                # wos=WOUtility.doPaging(request,companies)
                wos=companies[:50]
                serializer = WOSerializer2(wos, many=True)
                return Response(serializer.data)
            else:
                content = {'message': 'Error'}
                # print(content)
                return Response(content)
class SysUserView(APIView):



    def createDjangoUser(self,user):
        djangoUser = User.objects.create_user(username=user['fullName'],
                               email=user['email'],
                                  password=user['password'])
        return djangoUser.id
    def post(self,request):
        try:

            u_id=self.createDjangoUser(request.data)

            serializer=SysUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.userId=User.objects.get(id=u_id)
                # print(serializer)

                uu=serializer.save()
                uu.userId=User.objects.get(id=u_id)
                uu.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                content = {'message': serializer.errors}
                # print(content)
                return Response(content)
        except Exception as e:


            # else:
                content = {'message': str(e)}
                # print(content)
                return Response(content)
class SiteView(APIView):




    def get(self,request):
            sites=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1).exclude(id__in=AssetException.objects.all().values_list('assetExceptionAsset',flat=True))
            my_site=MiniAssetSerializer(sites, many=True)
            return Response(my_site.data)
class SubSiteView(APIView):




    def get(self,request,id):
            sites=Asset.objects.filter(Q(assetIsLocatedAt__id=id)|Q(assetIsPartOf__id=id)).filter(assetTypes=1)
            my_site=MiniAssetSerializer(sites, many=True)
            return Response(my_site.data)
