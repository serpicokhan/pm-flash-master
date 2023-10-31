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
from cmms.forms import AssetForm,WoAssetForm,AssetListForm
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
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
from django.db.models import Q
from django.db import  transaction
from django.db.models import Count



def filterUser(request):
    main_asset=request.GET.get('main_asset',False)
    search_term=request.GET.get('search',False)





    user1=SysUser.objects.get(userId=request.user)
    books=Asset.objects.none()
    if(( not user1.userId.groups.filter(name__in= ('manager','operator')).exists())):
        books = Asset.objects.filter(Q(id__in=AssetUser.objects.filter(AssetUserUserId__userId=request.user).values_list('id',flat=True))|Q(assetIsLocatedAt__id__in=AssetUser.objects.filter(AssetUserUserId__userId=request.user).values_list('id',flat=True))|Q(assetIsPartOf__id__in=AssetUser.objects.filter(AssetUserUserId__userId=request.user).values_list('id',flat=True))).order_by('-id')
    else:
        books=Asset.objects.all().order_by('-id')
    if(main_asset):
            print('mainasset',main_asset)
            books=books.filter(Q(assetIsLocatedAt__id=main_asset)|Q(assetIsPartOf__id=main_asset)|Q(id=main_asset))
    return books
def filterUserByResult(request,books):
    # books=Asset.objects.none()
    if(not request.user.groups.filter(name__in= ('manager','operator')).exists()):
        books = books.filter(Q(id__in=AssetUser.objects.filter(AssetUserUserId__userId=request.user).values_list('id',flat=True))|Q(assetIsLocatedAt__id__in=AssetUser.objects.filter(AssetUserUserId__userId=request.user).values_list('id',flat=True))|Q(assetIsPartOf__id__in=AssetUser.objects.filter(AssetUserUserId__userId=request.user).values_list('id',flat=True))).order_by('-id')
    else:
        pass
    return books

@permission_required('cmms.view_asset')
def list_asset(request,id=None):
    books=[]
    dc={}
    form=AssetListForm()
    books =filterUser(request)
    # print(123)
    sort_type=request.GET.get('sort',False)
    sort_arrow=request.GET.get('asc',False)
    main_asset=request.GET.get('main_asset',False)
    search_term=request.GET.get('search',False)

    kvm=0
    if(main_asset):
        # print('mainasset',main_asset)
        books=books.filter(Q(assetIsLocatedAt__id=main_asset)|Q(assetIsPartOf__id=main_asset))
        dc['main_asset']=main_asset

    if(search_term):
        books=AssetUtility.seachAsset(kvm,search_term)
        dc['search']=search_term
        dc['kvm']=kvm
    # dc={'asset': wos,'section':'list_asset','page':page}
    if(sort_type):
        if(sort_type=='1'):
            if(sort_arrow=='asc'):
                books=books.order_by('assetName')
            else:
                books=books.order_by('-assetName')
        if(sort_type=='2'):
            if(sort_arrow=='asc'):
                books=books.order_by('assetCode')
            else:
                books=books.order_by('-assetCode')
        if(sort_type=='3'):
            if(sort_arrow=='asc'):
                books=books.order_by('assetStatus')
            else:
                books=books.order_by('-assetStatus')
        if(sort_type=='4'):
            if(sort_arrow=='asc'):
                books=books.order_by('assetCategory')
            else:
                books=books.order_by('-assetCategory')
        if(sort_type=='5'):
            if(sort_arrow=='asc'):
                books=books.order_by('assetIsLocatedAt')
            else:
                books=books.order_by('-assetIsLocatedAt')
        # wos,page=AssetUtility.doPagingWithPage(request,books)



        dc['sort']=sort_type
        dc['asc']=sort_arrow



    wos,page=AssetUtility.doPagingWithPage(request,books)
    dc['asset']=wos
    dc['section']='list_asset'
    dc['page']=page
    # main_asset=Asset.objects.filter(assetIsLocatedAt__isnull=True)
    dc['form']=form
    return render(request, 'cmms/asset/assetList.html', dc)




@permission_required('cmms.view_asset')
def list_asset_location(request):
    books=[]
    books =filterUser(request).filter(assetTypes=1).order_by('-assetName')
    wos,page=AssetUtility.doPagingWithPage(request,books)
    # return render(request, 'cmms/asset/assettreeList.html', {'asset': wos,'section':'list_asset_location','page':page})
    books=Asset.objects.filter(assetTypes=1)
    return render(request, 'cmms/asset/assetList.html', {'asset': wos,'section':'list_asset_location','page':page})

@permission_required('cmms.view_asset')
def list_asset_machine(request):
    books=[]
    books =filterUser(request).filter(assetTypes=2).order_by('-assetName')
    wos,page=AssetUtility.doPagingWithPage(request,books)
    return render(request, 'cmms/asset/assetList.html', {'asset': wos,'section':'list_asset_machine','page':page})

@permission_required('cmms.view_asset')
def list_asset_tool(request):
    books=[]
    books =filterUser(request).filter(assetTypes=3).order_by('-assetName')
    wos,page=AssetUtility.doPagingWithPage(request,books)
    return render(request, 'cmms/asset/assetList.html', {'asset': wos,'section':'list_asset_tool','page':page})

##########################################################

def save_asset_form(request, form, template_name,id=None,page=None):
    data = dict()

    os=Asset.objects.get(id=id)
    # print("Asset From asset status {}".format(os.assetStatus))
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            main_asset= request.POST.get('main_asset',False)
            data['form_is_valid'] = True
            books = filterUser(request)
            # if(main_asset):
            #     books=books.filter(Q(assetIsLocatedAt__id=main_asset)|Q(assetIsPartOf__id=main_asset))
            # print("save asset page",page)
            AssetUtility.log(request,form,id)
            # print(1)
            # page=request.GET.get('page',1)
            wos,page=AssetUtility.doPagingWithPage(request,books)
            data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
                'asset': wos,
                'perms': PermWrapper(request.user),
                'page':page if page is not None else 1
            })
            data['html_asset_paging'] = render_to_string('cmms/asset/asset_sort.html', {
                'asset': wos,

                'perms': PermWrapper(request.user),
                'page':page if page is not None else 1
            })
        else:
            print(form.errors)
            data['form_is_valid'] = False
    # print(page,"!!!!!!!!!!!!!!")
    main_asset=request.GET.get('main_asset',False)
    context = {'form': form,'lId':id,'page':page if page is not None else 1,'main_asset':main_asset}

    data['html_asset_form'] = render_to_string(template_name, context, request=request)
    data['id']=id
    return JsonResponse(data)
##########################################################
def asset_delete(request, id):
    comp1 = get_object_or_404(Asset, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        # books =filterUser(request)
        # wos=AssetUtility.doPaging(request,books)
        #Tasks.objects.filter(assetId=id).update(asset=id)


        # data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
        #     'asset': wos,
        #     'perms': PermWrapper(request.user)
        # })
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
        # print("!!!!!!!!!!!!!!!!!!!!!!12")
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
    page=request.GET.get('page',1)
    print("update page",page)
    # print("asset status:{}".format(company.assetStatus))
    template=""
    if (request.method == 'POST'):

        form = AssetForm(request.POST, instance=company)
    else:
        assetcatText=company.assetCategory.name if company.assetCategory else ''
        form = AssetForm(instance=company,initial={'asseccategorytxt':assetcatText,'assetispart':company.assetIsPartOf})
    if(company.assetTypes==1):
        template="cmms/asset/partialAssetLocationUpdate.html"
    elif(company.assetTypes==2):
        template="cmms/asset/partialAssetMachineUpdate.html"
    else:
        template="cmms/asset/partialAssetToolUpdate.html"

    return save_asset_form(request, form,template,id,page=page)
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
        books =Asset.objects.all().order_by('-id')
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
def duplicate_asset(request,id):
    data=dict()
    if (request.method == 'POST'):
        assetId=request.POST.get("assetID","")
        tedad=request.POST.get("tedad","")
        pishvand=request.POST.get("pishvand","")
        partof=request.POST.getlist("partof")
        if(len(partof)>0):
            partof=True
        else:
            partof=False




        try:
            with transaction.atomic():

                for i in range(1,int(tedad)+1):
                    AssetUtility.duplicate_asset(id,i,pishvand,partof)
        except Exception as e:
            data['error']="خطا در ثبت اطلاعات"
            print(e)



        books=[]
        books =Asset.objects.all().order_by('-id')
        wos=AssetUtility.doPaging(request,books)
        data['form_is_valid']=True
        data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
            'asset': wos,
            'perms': PermWrapper(request.user)
        })
        # list_asset(request)


    else:
        m=Asset.objects.get(id=id)
        context={'form':m,'perms': PermWrapper(request.user)}
        data["modalassetcat"]=render_to_string('cmms/asset/assetDuplicateForm.html',
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
def asset_search(request,kvm):

    q=request.GET.get("q","")
    page=request.GET.get('page',1)
    main_asset=request.GET.get('main_asset',False)
    # print('asset  page',page,q)
    data=dict()
    # print(kvm,'///',q)
    books=AssetUtility.seachAsset(kvm,q)
    if(main_asset):
        books=books.filter(Q(assetIsLocatedAt__id=main_asset)|Q(assetIsPartOf__id=main_asset))
    books=filterUserByResult(request,books)
    wos=AssetUtility.doPaging(request,list(books))
    data['html_asset_search_tag_list'] = render_to_string('cmms/asset/partialAssetList.html', {
                   'asset': wos,'page':page                      ,'perms': PermWrapper(request.user) })
    data['html_asset_paginator'] = render_to_string('cmms/asset/partialAssetPagination.html', {
                      'asset': wos,'pageType':'list_asset','ptr':kvm,'search':q,'main_asset':main_asset})
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
        r.append({'elat':str(i.assetCauseCode),'start':str(i.assetOfflineFromTime)+' '+str(i.getdate()).replace('-','/'),'end':str(i.assetOnlineFromTime)+' '+str(i.getonlinedate()).replace('-','/')})


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
        assets=Asset.objects.filter(assetCategory=i,assetTypes=2,assetIsLocatedAt__isnull=False).order_by('assetName')
        x2=[]
        x4=[]
        x5=[]
        for x in assets:

            x2.append('{}:{}'.format(x.assetCode,x.assetName))
            x4.append(x.id)
            x5.append(x.assetStatus)
        x3.append(zip(x2,x4,x5))
    final_list=zip(x1,x3,x0)
    a_zip=zip(x1,x0)

    assetloc=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1)
            # acat_dict[i.name][x.id]=x.assetName
        # x1.push(x2)
        # x2=[]
    return render(request, 'cmms/asset/dash2.html', {'assets':final_list,'test':a_zip,'locs':assetloc,'section':'dashasset'})
def tmp_doPaging(request,books):
        page=request.GET.get('page',1)
        paginator = Paginator(books, 10)
        wos=None
        try:
            wos=paginator.page(page)
        except PageNotAnInteger:
            wos = paginator.page(1)
        except EmptyPage:
            wos = paginator.page(paginator.num_pages)
        return wos
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
    children=Asset.objects.filter(Q(assetIsPartOf=id)|Q(assetIsLocatedAt=id))
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
@csrf_exempt
def create_rowasset(request,wo):
    data=dict()
    books=Asset.objects.filter(Q(assetIsLocatedAt=wo))

    data['html_assetAsset_list']= render_to_string('cmms/asset/asset/partialAssetRow.html', {
        'assetwos': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)
def list_assetAsset(request,id):
    data=dict()
    books=Asset.objects.filter(Q(assetIsLocatedAt=id)|Q(assetIsPartOf=id)).order_by('assetName')

    data['html_assetAsset_list']= render_to_string('cmms/asset/asset/partialAssetRow.html', {
        'assetwos': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)

@csrf_exempt
def asset_getAssets(request):
    searchStr= request.GET['qry'] if request.GET['qry'] else ''
    x=list(AssetUtility.getAssets(searchStr))
    return JsonResponse(x, safe=False)
@csrf_exempt
def assetAsset_craete(request):

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['main']=body['lastAssetid']
        data['child']=body['assetAssetId']
        form = data
        child_asset_id= data['child']
        main_asset_id= data['main']
        main_asset=Asset.objects.get(id=main_asset_id)
        print(main_asset)
        child_asset=Asset.objects.get(id=child_asset_id)
        if(main_asset.assetTypes==1):
            print("hrere")
            child_asset.assetIsLocatedAt=main_asset
            child_asset.save()
        else:
            child_asset.assetIsPartOf=main_asset
            child_asset.save()
        data=dict()
        books=Asset.objects.filter(Q(assetIsLocatedAt=main_asset))
        data['html_assetAsset_list']= render_to_string('cmms/asset/asset/partialAssetRow.html', {
            'assetwos': books,
            'perms': PermWrapper(request.user)
        })
        data['form_is_valid']=True
        return JsonResponse(data)

    else:
        form = None
        data=dict()
        data['html_assetAsset_form']= render_to_string('cmms/asset_asset/partialAssetAssetCreate.html', {

        })

        return JsonResponse(data)
@csrf_exempt
def assetAsset_delete(request,id,child):
    # print(request.GET['q'])

    main_asset=Asset.objects.get(id=id)
    child_asset=Asset.objects.get(id=ch_id)
    # if(main_asset.assetTypes==1):
    if(child_asset.assetIsLocatedAt==main_asset):
        child_asset.assetIsLocatedAt=None
        child_asset.save()
    else:
        child_asset.assetIsPartOf=None
        child_asset.save()
    data=dict()
    books=Asset.objects.filter(Q(assetIsLocatedAt=main_asset)|Q(assetIsPartOf=main_asset))

    data['html_assetAsset_list']= render_to_string('cmms/asset/asset/partialAssetRow.html', {
        'assetwos': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)


    # if(len(x)==0):
    #     print("dasdsa")
    #     x=[{'id':-1,'partName':'قطعه یافت نشد'}]


    # response_data = {}
    # response_data['result'] = '[dsadas,dasdasdas]'
    return JsonResponse(x, safe=False)





@csrf_exempt
def clone_asset(request,ids):
    clean_data=[int(i)  for i in ids.split(',')]
    for id in  clean_data:
            AssetUtility.clone_asset(id)

    data=dict()
    books = Asset.objects.all().order_by('-id')
    page=request.GET.get('page',1)
    wos=AssetUtility.doPaging(request,books)
    data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
        'asset': wos,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid'] = True
    print('done')
    return JsonResponse(data)

@csrf_exempt
def bulk_delete_asset(request,ids):
    clean_data=[int(i)  for i in ids.split(',')]
    foo=Asset.objects.filter(id__in=clean_data)
    for i in foo:
        i.delete()
    data=dict()
    books = Asset.objects.all().order_by('-id')
    page=request.GET.get('page',1)
    wos=AssetUtility.doPaging(request,books)
    data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
        'asset': wos,
        'perms': PermWrapper(request.user)
    })

    data['html_asset_paginator'] = render_to_string('cmms/asset/partialAssetPagination_none.html', {
                      'asset': wos})
    data['form_is_valid'] = True
    # print('done')
    return JsonResponse(data)

@csrf_exempt
def create_woasset(request):

    data2=dict()
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['assetTypes']=body['assetTypes']
        data['assetName']=body['assetName']
        data['assetCode']=body['assetCode']
        data['assetIsPartOf']=body['assetIsPartOf']
        data['assetIsLocatedAt']=body['assetIsLocatedAt']
        form = WoAssetForm(data)
        if form.is_valid():
           form.save()
           data2['form_is_valid'] = True
           data2['woasset_id']=form.instance.id
           data2['woasset_name']=form.instance.assetName
           return JsonResponse(data2)
        else:
           pass
    else:
           form = AssetForm()
           context={'form':form}
           data2['html_asset_form'] = render_to_string('cmms/asset/woasset/woasset_create.html',
               context,
               request=request,
           )
           return JsonResponse(data2)


def assetloadinfo(request):
    data=dict()
    makan=request.GET.get("makan","")
    noe=request.GET.get("noe","-1")


    if(makan):
        assets=Asset.objects.none()
        if(makan== '-1'):
            assets=Asset.objects.all()
        else:
            assets=Asset.objects.filter(assetIsLocatedAt=makan)
        if(len(noe)==0  or( "null" in noe and len(noe)==1) or noe=="-1" or noe=="undefined" or noe=="0"):
            pass
        else:
            cats=[int(i)  for i in noe.split(',')]
            asset_cats=AssetCategory.objects.filter(id__in=cats)
            sub_cats=[]
            for cat in asset_cats:
                sub_cats.append(cat)
                sub_cats=sub_cats+cat.get_all_child_categories()
            # print(len(noe),noe)
            assets=assets.filter(assetCategory__in=sub_cats)
        data["html_assets_dynamics"]=render_to_string('cmms/maintenance/partialWOAssetDynamics.html',
            {'assets':assets})
        data["form_is_valid"]=True
    return JsonResponse(data)

def gen_asset_code(request,id):
    x=Asset.objects.get(id=id)
    loc_code=request.GET.get('loc','-1')
    pishvand=request.GET.get('pishvand','')
    if(loc_code!= '-1' and len(pishvand)>0):
        loc=Asset.objects.get(id=int(loc_code))
        max_digit=Asset.objects.filter(assetCode__contains="{}-{}-{}".format(loc.get_asset_loc_code(),x.assetCategory.code,pishvand)).count()
        code="{}-{}-{}{}".format(loc.get_asset_loc_code(),x.assetCategory.code,pishvand,max_digit+1)
    elif(loc_code!= '-1' and len(pishvand)==0):
        loc=Asset.objects.get(id=int(loc_code))
        max_digit=Asset.objects.filter(assetCode__contains="{}-{}".format(loc.get_asset_loc_code(),x.assetCategory.code)).count()
        code="{}-{}-{}".format(loc.get_asset_loc_code(),x.assetCategory.code,max_digit+1)

    else:
        max_digit=Asset.objects.filter(assetCode__contains="{}-{}".format(x.get_asset_loc_code(),x.assetCategory.code)).count()
        code="{}-{}-{}".format(x.get_asset_loc_code(),x.assetCategory.code,max_digit+1)

    return JsonResponse({'code':code,'form_is_valid':True},safe=False)

def asset_sort(request,id):
    data=dict()
    sort_name=request.GET.get('e',False)
    asset=Asset.objects.none()
    search_term=request.GET.get('search',False)
    kvm=request.GET.get('kvm',False)
    main_asset=request.GET.get('main_asset',False)

    if(search_term):
        asset=AssetUtility.seachAsset(kvm,search_term)
    else:
        asset=Asset.objects.all()
    if(main_asset):
        asset=asset.filter(Q(assetIsLocatedAt__id=main_asset)|Q(assetIsPartOf__id=main_asset))
    if(id=='1'):
        print(sort_name)
        if(sort_name=='asc'):
            asset=asset.order_by('assetName')
        else:
            asset=asset.order_by('-assetName')

    elif(id=='2'):
        if(sort_name=='asc'):
            asset=asset.order_by('assetCode')
        else:
            asset=asset.order_by('-assetCode')
    elif(id=='3'):
        if(sort_name=='asc'):
            asset=asset.order_by('assetStatus')
        else:
            asset=asset.order_by('-assetStatus')
    elif(id=='4'):
        if(sort_name=='asc'):
            asset=asset.order_by('assetCategory')
        else:
            asset=asset.order_by('-assetCategory')
    elif(id=='5'):

        if(sort_name=='asc'):
            asset=asset.order_by('assetIsLocatedAt')
        else:
            asset=asset.order_by('-assetIsLocatedAt')
    wos,page=AssetUtility.doPagingWithPage(request,asset)
    data['html_asset_list'] = render_to_string('cmms/asset/partialAssetList.html', {
        'asset': wos,
        'perms': PermWrapper(request.user),
        'page':page if page is not None else 1
    })
    data['html_asset_paging'] = render_to_string('cmms/asset/asset_sort.html', {
        'asset': wos,
        'sort':id,
        'asc':sort_name,
        'search':search_term,
        'kvm':kvm,
        'perms': PermWrapper(request.user),
        'page':page if page is not None else 1,
        'main_asset':main_asset
    })
    return JsonResponse(data)

def getRelatedAsset(request,id):
    data=dict()
    assets=Asset.objects.filter(assetIsLocatedAt__id=id)
    data["pval"]=render_to_string('cmms/maintenance/partialWOAssetDynamics.html',
        {'assets':assets})
    data["form_is_valid"]=True
    return JsonResponse(data)

@api_view(['GET'])
def asset_collection(request):
    if request.method == 'GET':
        posts = Asset.objects.all()
        serializer = AssetSerializer(posts, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def asset_Stop_count(request,id):
    if request.method == 'GET':

        assetList=Asset.objects.filter(assetIsLocatedAt__id=id).values_list('id',flat=True)
        s1,s2=[],[]
        z1,z2=[],[]
        offlineCountByEvent=AssetUtility.getOfflineCountByEventAPI(assetList)
        for i in offlineCountByEvent:
            s1.append({'date':i.id,'value':i.eventname})
        return JsonResponse(s1,safe=False)
@api_view(['GET'])
def asset_category_api(request,id):
    if request.method == 'GET':
        # posts = Asset.objects.all()
        asset_categories = AssetCategory.objects.filter(asset__assetIsLocatedAt__id=id).annotate(asset_count=Count('asset')).values('id','name', 'asset_count').filter(asset_count__gt=0)
        # filtered_categories = asset_categories.filter(asset=id)
        serializer = AssetCategorySerializer2(asset_categories, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def location_collection(request):
    if request.method == 'GET':
        posts = Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1)
        serializer = MiniAssetSerializer(posts, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def machine_collection(request,id,catid):
    if request.method == 'GET':
        posts = Asset.objects.filter(assetIsLocatedAt__id=id,assetCategory__id=catid)
        serializer = MiniAssetSerializer(posts, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def location_details(request,id):
    if request.method == 'GET':
        posts = Asset.objects.get(id=id)
        serializer = AssetSerializer(posts)
        return Response(serializer.data)
@api_view(['GET'])
def assetwo_collection(request,id):
    if request.method == 'GET':
        print("asset wo")
        posts = WorkOrder.objects.filter(woAsset=id)
        serializer = WOSerializer(posts, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def asset_detail_collection(request,id):
    if request.method == 'GET':
        print(id,"id")
        posts = Asset.objects.get(id=id)
        serializer = AssetSerializer(posts)
        return Response(serializer.data)

@csrf_exempt
def get_json_test(request):
    jsonData = {
          "nodeID": {
            "1": [

               {"ID": "1.1",
                "childNodeType": "branch",
                "childData": [
                  "1.1: column 1",
                  "1.1: column 2"
                  ]
              },
              {"ID": "1.2",
                "childNodeType": "leaf",
                "childData": [
                  "1.2: column 1",
                  "1.2: column 2"
                  ]
              },
              {"ID":"1.3",
                "childNodeType": "leaf",
                "childData": [
                  "1.3: column 1",
                  "1.3: column 2"
                  ]
              }

            ],
            "1.1": [

                {"ID":"1.1.1",
                  "childNodeType": "leaf",
                  "childData": [
                    "1.1.1: column 1",
                    "1.1.1: column 2"
                    ]
                },
                {"ID":"1.1.2",
                  "childNodeType": "leaf",
                  "childData": [
                    "1.1.2: column 1",
                    "1.1.2: column 2"
                    ]
                }

            ],
            "2": [

                {"ID":"2.1",
                  "childNodeType": "leaf",
                  "childData": [
                    "2.1: column 1",
                    "2.1: column 2"
                    ]
                },
                {"ID":"2.2",
                  "childNodeType": "leaf",
                  "childData": [
                    "2.2: column 1",
                    "2.2: column 2"
                    ]
                },
                {"ID":"2.3",
                  "childNodeType": "leaf",
                  "childData": [
                    "2.3: column 1",
                    "2.3: column 2"
                    ]
                }

            ],
            "3": [

                {"ID":"3.1",
                  "childNodeType": "leaf",
                  "childData": [
                    "3.1: column 1",
                    "3.1: column 2"
                    ]
                },
                {"ID":"3.2",
                  "childNodeType": "leaf",
                  "childData": [
                    "3.2: column 1",
                    "3.2: column 2"
                    ]
                },
                {"ID":"3.3",
                  "childNodeType": "leaf",
                  "childData": [
                    "3.3: column 1",
                    "3.3: column 2"
                    ]
                }

            ]
          }
        };
    return JsonResponse(jsonData)
def assetExport(request):
    search=request.GET.get('search',False)
    kvm=request.GET.get('kvm',False)
    main_asset=request.GET.get('main_asset',False)
    asset=Asset.objects.all()
    if(main_asset):
        asset=asset.filter(Q(assetIsLocatedAt__id=main_asset)|Q(assetIsPartOf__id=main_asset))
    if(search):
        asset=AssetUtility.searchAsset(kvm,search)
    data = AssetUtility.download_csv(request, asset)
    return HttpResponse (data, content_type='text/csv')
def assetImport(request):
    return render(request, 'cmms/asset/assetUpload.html', {})
def upload_file_asset(request):
    def iter_rows(ws):
        for row in ws.iter_rows():
            yield [cell.value for cell in row]
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        data=dict()

        return JsonResponse(data)
    return JsonResponse({'post':'fasle'})

def get_location(request):
    locations=Asset.objects.filter(assetIsLocatedAt__isnull=True).values_list('id','assetName')
    location_data = []
    for location_id, location_name in locations:
        location_data.append({
            'id': location_id,
            'text': location_name,
            'type': 'location',
            'children': True  # You can modify this based on your application logic
        })

    return JsonResponse(location_data, safe=False)

def get_asset_child(request):
    id=request.GET.get("locationId",False)
    if(id):
        child_assets=Asset.objects.filter(assetIsLocatedAt__id=id).values_list('id','assetName')
        location_data = []
        for location_id, location_name in child_assets:
            location_data.append({
                'id': location_id,
                'text': location_name,
                'type': 'Machines',
                'children': True  # You can modify this based on your application logic
            })
        return JsonResponse(location_data, safe=False)
    return JsonResponse({})
def get_tree_asset_view(request):
    data=dict()
    wos=Asset.objects.filter(assetTypes=1,assetIsLocatedAt__isnull=True).order_by('assetName')
    page=1
    data['html_table_view']=render_to_string('cmms/asset/partialTreeTable.html', {
        'asset': wos,
        'perms': PermWrapper(request.user),
        'page':page if page is not None else 1
    })
    return JsonResponse(data)
def load_child_tree_info(request):
    id=request.GET.get("assetId",False)
    if(id):
        asset=Asset.objects.filter(Q(assetIsLocatedAt__id=id)|Q(assetIsPartOf__id=id))
        data=dict()
        page=1
        data['html_table_view2']=render_to_string('cmms/asset/partialTreeTable.html', {
            'asset': asset,
            'perms': PermWrapper(request.user),
            'page':page if page is not None else 1
        })
        return JsonResponse(data)
