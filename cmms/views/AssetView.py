'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neassetbject.OrderId.id)
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
from django.core.paginator  import *
from cmms.models.Asset import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.paginator  import *
from cmms.business.AssetUtility import AssetUtility
from cmms.business.mttr import *
from cmms.business.WOUtility import *
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
@permission_required('cmms.view_assets')
def list_asset(request,id=None):

    #print("username {}".format(request.user.username))
    # if(request.user.username=="admin"):
    books=[]
    books =Asset.objects.all().order_by('-id')
    wos=AssetUtility.doPaging(request,books)
    return render(request, 'cmms/asset/assetList.html', {'asset': wos})
    # else:
    #      return HttpResponseRedirect(reverse('list_dashboard' ))
    #paging




@permission_required('cmms.view_assets')
def list_asset_location(request):
    books=[]
    books =Asset.objects.filter(assetTypes=1).order_by('-assetName')
    wos=AssetUtility.doPaging(request,books)
    return render(request, 'cmms/asset/assetList.html', {'asset': wos})
    # books=Asset.objects.filter(assetTypes=1)
    # return render(request, 'cmms/asset/assetList.html', {'asset': books})

@permission_required('cmms.view_assets')
def list_asset_machine(request):
    books=[]
    books =Asset.objects.filter(assetTypes=2).order_by('-assetName')
    wos=AssetUtility.doPaging(request,books)
    return render(request, 'cmms/asset/assetList.html', {'asset': wos})

@permission_required('cmms.view_assets')
def list_asset_tool(request):
    books=[]
    books =Asset.objects.filter(assetTypes=3).order_by('-assetName')
    wos=AssetUtility.doPaging(request,books)
    return render(request, 'cmms/asset/assetList.html', {'asset': wos})

##########################################################

def save_asset_form(request, form, template_name,id=None):
    data = dict()
    os=Asset.objects.get(id=id)
    # print("Asset From asset status {}".format(os.assetStatus))
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()

            data['form_is_valid'] = True
            books = Asset.objects.all().order_by('-assetName')
            page=request.GET.get('page',1)
            wos=AssetUtility.doPaging(request,books)
            data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
                'asset': wos,
                'perms': PermWrapper(request.user)
            })
        else:
            print(form.errors)
            data['form_is_valid'] = False
    context = {'form': form,'lId':id}
    data['html_asset_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def asset_delete(request, id):
    comp1 = get_object_or_404(Asset, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books =Asset.objects.all().order_by('-assetName')
        wos=AssetUtility.doPaging(request,books)
        #Tasks.objects.filter(assetId=id).update(asset=id)


        data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
            'asset': wos,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'asset': comp1}
        data['html_asset_form'] = render_to_string('cmms/asset/partialAssetDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def asset_create_location(request):
    if (request.method == 'POST'):
        form = AssetForm(request.POST)
        return save_asset_form(request, form, 'cmms/asset/partialAssetLocationCreate.html')
    else:
        assetInstance=Asset.objects.create(assetTypes=1)
        form = AssetForm(instance=assetInstance,initial= {'assetHasPartOf':'False','assetStatus':'True','assetTypes':'1'})
        return save_asset_form(request, form, 'cmms/asset/partialAssetLocationCreate.html',assetInstance.id)

def asset_create_machine(request):
    if (request.method == 'POST'):
        form = AssetForm(request.POST)
        return save_asset_form(request, form, 'cmms/asset/partialAssetMachineCreate.html')
    else:
        assetInstance=Asset.objects.create(assetTypes=2)
        form = AssetForm({'assetHasPartOf':'False','assetStatus':'True','assetTypes':'2'})
        return save_asset_form(request, form, 'cmms/asset/partialAssetMachineCreate.html',assetInstance.id)

def asset_create_tool(request):
    if (request.method == 'POST'):
        form = AssetForm(request.POST)
        return save_asset_form(request, form, 'cmms/asset/partialAssetToolCreate.html')
    else:
        assetInstance=Asset.objects.create(assetTypes=3)
        form = AssetForm({'assetHasPartOf':'False','assetStatus':'True','assetTypes':'3'})
        return save_asset_form(request, form, 'cmms/asset/partialAssetToolCreate.html',assetInstance.id)




##########################################################
def asset_update(request, id):
    company= get_object_or_404(Asset, id=id)
    # print("asset status:{}".format(company.assetStatus))
    template=""
    if (request.method == 'POST'):
        form = AssetForm(request.POST, instance=company)
    else:
        assetcatText=company.assetCategory.name if company.assetCategory else ''
        form = AssetForm(instance=company,initial={'asseccategorytxt':assetcatText})
    if(company.assetTypes==1):
        template="cmms/asset/partialAssetLocationUpdate.html"
    elif(company.assetTypes==2):
        template="cmms/asset/partialAssetMachineUpdate.html"
    else:
        template="cmms/asset/partialAssetToolUpdate.html"

    return save_asset_form(request, form,template,id)
##########################################################

##########################################################
def asset_type_selector(request,ids=None):
    # data=dict()
    # clean_data=[int(i)  for i in ids.split(',')]
    #
    # if (request.method == 'POST'):
    #
    #
    #
    # else:
    #     data=dict()
    #     context={'cat':m,'perms': PermWrapper(request.user),'ids':ids}
    #     data["form_asset_selector"]=render_to_string('cmms/asset/assetType.html',
    #         context,
    #         request=request)
    #
    #     return JsonResponse(data)
    data=dict()
    data['form_asset_selector']= render_to_string('cmms/asset/assetType.html')
    return JsonResponse(data)
###########################
def get_assetCategory(request):
    data=dict()
    '''render_to_string('cmms/asset/temp.txt')'''
    m=AssetUtility.getCategory()

    m=m.replace('"',"'")
    data["modalassetcat"]=render_to_string('cmms/asset/assetcategoryselector.html',{'cat':m,'perms': PermWrapper(request.user)})
    return JsonResponse(data)
def get_assetCategoryMain(request,ids):
    clean_data=[int(i)  for i in ids.split(',')]

    data=dict()
    '''render_to_string('cmms/asset/temp.txt')'''
    if (request.method == 'POST'):
        assets=Asset.objects.filter(id__in=clean_data)
        catId=request.POST.get("assetCat2")
        # print(catId,"cat***************************")
        for s in assets:
            s.assetCategory=AssetCategory.objects.get(id=int(catId))
            s.save()
        books=[]
        books =Asset.objects.all().order_by('-assetName')
        wos=AssetUtility.doPaging(request,books)
        data['form_is_valid']=True
        data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
            'asset': wos,
            'perms': PermWrapper(request.user)
        })


    else:

        m=AssetUtility.getCategory()
        m=m.replace('"',"'")
        context={'cat':m,'perms': PermWrapper(request.user),'ids':ids}
        data["modalassetcat"]=render_to_string('cmms/asset/assetcategoryselectorMain.html',
        context,
        request=request)
    return JsonResponse(data)
def get_location_by_category(request):
    data=dict()
    '''render_to_string('cmms/asset/temp.txt')'''
    m=AssetUtility.getLocationCategory()

    m=m.replace('"',"'")
    data["modalassetcat"]=render_to_string('cmms/asset/locationcategoryselector.html',{'cat':m,'perms': PermWrapper(request.user)})
    return JsonResponse(data)
#######################Search By tags#####################
def asset_search(request,kvm,searchStr):
    data=dict()
    # print("1232321321")
    searchStr=searchStr.replace("__"," ")
    # print(kvm,"$$$$$$$$$$$$$")
    books=AssetUtility.seachAsset(kvm,searchStr)
    wos=AssetUtility.doPaging(request,list(books))
    data['html_asset_search_tag_list'] = render_to_string('cmms/asset/partialAssetList.html', {
                   'asset': wos                      ,'perms': PermWrapper(request.user) })
    data['html_asset_paginator'] = render_to_string('cmms/asset/partialAssetPagination.html', {
                      'asset': wos,'pageType':'asset_search','ptr':kvm,'pt2':searchStr})
    data['form_is_valid'] = True
    return JsonResponse(data)
#######################Search#####################
def asset_mttr(request,id):
    data=dict()
    # print(MTTR.getTotalMTTR(id)[0].id,"########")
    data['asset_mttr']='{:0.2f}'.format(MTTR.getTotalMTTR(id)[0].id if MTTR.getTotalMTTR(id)[0].id else 0 )
    return JsonResponse(data)
def asset_mtbf(request,id):
    data=dict()
    # print(MTTR.getTotalMTTR(id)[0].id,"########")
    data['asset_mtbf']='{:0.2f}'.format(MTTR.getTotalMTBF(id)[0].id if MTTR.getTotalMTBF(id)[0].id else 0 )
    return JsonResponse(data)
def asset_status(request,id):
    data=dict()
    # print(MTTR.getTotalMTTR(id)[0].id,"########")
    data['asset_overdue']='{:0.2f}'.format(WOUtility.getOverdueWoAsset(id)[0].id if WOUtility.getOverdueWoAsset(id)[0].id    else 0 )
    data['asset_wait4part']='{:0.2f}'.format(WOUtility.getWait4PartWoAsset(id)[0].id if WOUtility.getWait4PartWoAsset(id)[0].id    else 0 )
    data['asset_openwo']='{:0.2f}'.format(WOUtility.getOpenWoAsset(id)[0].id if WOUtility.getOpenWoAsset(id)[0].id    else 0 )
    return JsonResponse(data)
def asset_offline_status(request,id):
    data=dict()
    # print("*******dsadsa***************")
    # start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=AssetUtility.getAssetOfflineStatus(id)
    n2=AssetUtility.getAssetOfflineStatusLine(id)
    n3=AssetLife.objects.filter(assetLifeAssetid__id=id).order_by('-assetOfflineFrom').first()
    recentBreak=AssetLife.objects.filter(assetLifeAssetid__id=id).order_by('-assetOfflineFrom')[:5]

    s1,s2=[],[]
    z1,z2=[],[]
    r=[]
    for i in n1:
        s1.append('{:.2f}'.format(i.id))
        s2.append(i.reason)
    for i in n2:
        z1.append('{:.2f}'.format(i.id))
        z2.append(i.month)
    for i in recentBreak:
        r.append({'elat':str(i.assetOfflineStatus),'start':str(i.assetOfflineFromTime)+' '+str(i.getdate()).replace('-','/'),'end':str(i.assetOnlineFromTime)+' '+str(i.getonlinedate()).replace('-','/')})


    data['html_assetOfflineStatus_list'] ={'woCompletedNum': s1,
                                    'woCompletedAssetId':s2,
                                    'lineAssetofflinecount':z1,'lineminthname':z2,'lastbreak':str(n3.assetOfflineFromTime)+' , '+str(n3.getdate()).replace('-','/') if n3 else '','recent':r
                                    }
    data['html_assetOffline_recent']=render_to_string('cmms/asset/lastbreak.html', {
        'breaks': r,'perms': PermWrapper(request.user)
    })
    return JsonResponse(data)
@csrf_exempt
def assetCancel(request,id):
    data=dict()
    if(request.method=='POST'):
        tg=Asset.objects.get(id=id)
        if(tg):
            if(not tg.assetName or not tg.assetCode or not tg.assetCategory):
                tg.delete()
                data['form_is_valid'] = True

    return JsonResponse(data)
##########################################################
def list_asset_dash(request):
    acat=AssetCategory.objects.all().order_by("priority")
    acat_dict={}
    x1=[]
    x0=[]
    # x2=[]
    x3=[]

    for i in acat:
        acat_dict[i.name]={}
        x0.append(i.id)
        x1.append(i.name)
        assets=Asset.objects.filter(assetCategory=i,assetTypes=2)
        x2=[]
        x4=[]
        x5=[]
        for x in assets:

            x2.append(x.assetName)
            x4.append(x.id)
            x5.append(x.assetStatus)
        x3.append(zip(x2,x4,x5))
    final_list=zip(x1,x3,x0)
    a_zip=zip(x1,x0)

    assetloc=Asset.objects.filter(assetIsLocatedAt__isnull=True)
            # acat_dict[i.name][x.id]=x.assetName
        # x1.push(x2)
        # x2=[]
    return render(request, 'cmms/asset/dash2.html', {'assets':final_list,'test':a_zip,'locs':assetloc})
#################################################################################

def js_list_asset_dash(request,locId):

    acat=AssetCategory.objects.all()
    data=dict()
    acat_dict={}
    x1=[]
    x0=[]
    # x2=[]
    x3=[]
    final_list=None
    a_zip=None

    for i in acat:
        acat_dict[i.name]={}

        assets=Asset.objects.filter(assetCategory=i,assetTypes=2,assetIsLocatedAt=locId)
        if(assets.count()>0):
            x0.append(i.id)
            x1.append(i.name)
            x2=[]
            x4=[]
            x5=[]
            for x in assets:

                x2.append(x.assetName)

                x4.append(x.id)
                x5.append(x.assetStatus)
            x3.append(zip(x2,x4,x5))
            final_list=zip(x1,x3,x0)
            a_zip=zip(x1,x0)

    # assetloc=Asset.objects.filter(assetIsLocatedAt__isnull=True)
            # acat_dict[i.name][x.id]=x.assetName
        # x1.push(x2)
        # x2=[]
    context={'perms': PermWrapper(request.user),'assets':final_list}
    data["html_asset_dash_list"]=render_to_string('cmms/asset/partialdash2.html',
        context,
        request=request)
    data["form_is_valid"]=True
    return JsonResponse(data)


###################################################################################



def show_asset_types(request,ids):

    clean_data=[int(i)  for i in ids.split(',')]

    data=dict()
    context={'perms': PermWrapper(request.user),'ids':ids}
    data["html_asset_type"]=render_to_string('cmms/asset/assetType_modal.html',
        context,
        request=request)
    return JsonResponse(data)

def asset_type_update(request,ids,cat):
    clean_data=[int(i)  for i in ids.split(',')]
    assets=Asset.objects.filter(id__in=clean_data)
    for i in assets:
        i.assetTypes=int(cat)
        i.save()
    data=dict()
    # print("update is ok")
    data["is_valid"]=True
    return JsonResponse(data)
def show_Asset_status(request,id):
    data=dict()

    wo=Asset.objects.none()
    if(id=="1"):
        wo=Asset.objects.filter(assetStatus=True).order_by("assetName")
    elif(id=="2"):
        wo=Asset.objects.filter(assetStatus=False).order_by("assetName")
    else:
        wo=Asset.objects.all().order_by("assetName")

    wos=AssetUtility.doPaging(request,wo)
    data['html_asset_search_tag_list'] = render_to_string('cmms/asset/partialAssetList.html', {
                   'asset': wos                      ,'perms': PermWrapper(request.user) })
    data['html_asset_paginator'] = render_to_string('cmms/asset/partialAssetPagination2.html', {
                      'asset': wos,'pageType':'show_Asset_status','ptr':id})
    data["form_is_valid"]=True
    return JsonResponse(data)
def show_asset_tree(request,id):
    children=Asset.objects.filter(assetIsPartOf=id)
    mainparts=AssetPart.objects.filter(assetPartAssetid=id)
    mainbooks2=BOMGroupPart.objects.filter(BOMGroupPartBOMGroup__in=
    BOMGroupAsset.objects.filter(BOMGroupAssetAsset=id).values_list('BOMGroupAssetBOMGroup',flat=True))
    a=[]
    for k in mainparts:
        test1={}
        test1["text"]=k.assetPartPid.partName
        a.append(test1)
    for k in mainbooks2:
        test1={}
        test1["text"]=k.BOMGroupPartPart.partName
        a.append(test1)


    for i in children:
        test1={}

        # test1[i.id]={}
        test1["text"]=i.assetName
        test1["cat"]=i.assetCategory.name
        test1["parrents"]=[]
        test1["parts"]=[]
        rt1=i.assetCategory
        parts=AssetPart.objects.filter(assetPartAssetid=i.id)
        books2=BOMGroupPart.objects.filter(BOMGroupPartBOMGroup__in=
        BOMGroupAsset.objects.filter(BOMGroupAssetAsset=i.id).values_list('BOMGroupAssetBOMGroup',flat=True))
        a1={}
        for k in parts:
            a1={}
            a1["text"]=k.assetPartPid.partName
            test1["parts"].append(a1)
        for k in books2:
            a1={}
            a1["text"]=k.BOMGroupPartPart.partName
            test1["parts"].append(a1)


        while(rt1.isPartOf):
            d1={}
            # test1[i.id]["rootcat"]=i.assetCategory.isPartOf.name
            d1["d1"]=rt1.isPartOf.name
            test1["parrents"].append(d1)
            rt1=rt1.isPartOf
        a.append(test1)
        test1={}



        # if(i.assetCategory.isPartOf):
        #     test1[i.id]["rootcat"]=i.assetCategory.isPartOf.name
    data=dict()
    data['form_is_valid']=True
    data['result']=render_to_string('cmms/asset/partialAssetTree.html', {
                      'assets': a})
    return JsonResponse(data)
@csrf_exempt
def js_list_assetWo(request,woId):
    data=dict()
    books=WorkOrder.objects.filter(woAsset=woId,isScheduling=False,visibile=True).exclude(woStatus__in=(7,8)).order_by('-id')

    data['html_assetWo_list']= render_to_string('cmms/asset_wo/partialAssetWoList.html', {
        'assetwos': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)
def js_list_assetSWo(request,woId):
    data=dict()
    books=Schedule.objects.filter(workOrder__in=WorkOrder.objects.filter(woAsset=woId
    ,isScheduling=True,running=True).values_list('id',flat=True)).order_by('-id')
    print(books)

    data['html_assetSWo_list']= render_to_string('cmms/asset_swo/partialAssetWoList.html', {
        'assetwos': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)
@csrf_exempt
def js_list_assetCloseWo(request,woId):
    data=dict()
    books=WorkOrder.objects.filter(woAsset=woId,woStatus__in=(7,8),isScheduling=False).order_by('-id')[:5]

    data['html_assetCloseWo_list']= render_to_string('cmms/asset_close_wo/partialAssetWoList.html', {
        'assetwos': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)
@csrf_exempt
def js_list_assetConsumedPart(request,woId):
    data=dict()
    books=WorkorderPart.objects.filter(woPartWorkorder=woId).order_by('-id')[:10]

    data['html_assetConsumedPart_list']= render_to_string('cmms/asset_consumed_part/partialAssetWoList.html', {
        'assetwos': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)
