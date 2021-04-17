from django.conf.urls import url
from django.urls import path
from cmms.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^tasks1/(?P<message>[-\w]+)/$', tasks, name='tasks'),
    url(r'^login/$', auth_views.login,{'template_name': 'cmms/registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'cmms/registration/logout.html'}, name='logout'),
   #url(r'^$',dashboard,name='dashboard'),
    url(r'^$',list_dashboard,name='list_dashboard'),
    url(r'^not_found/$',not_found,name='not_found'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/(?P<isScheduling>\d+)/GetCompletedWo/$', dash_GetCompletedWo, name='dash_GetCompletedWo'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetAllWorkOrders/$', dash_GetAllWorkOrders, name='dash_GetAllWorkOrders'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetResources/$', dash_getResource, name='dash_getResource'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetCompletedOpenStatus/$', dash_getWoByStatus, name='dash_getWoByStatus'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetCompletedWoDonat/$', dash_GetCompletedWoDonat, name='dash_GetCompletedWoDonat'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetDownTime/$', dash_getEquipDownTime, name='dash_getEquipDownTime'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetEquipCost/$', dash_getEquipCost, name='dash_getEquipCost'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetIstgahStatus/$', dash_getDashIstgahStatus, name='dash_getDashIstgahStatus'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetCauseCount/$', dash_getDashCauseCount, name='dash_getDashCauseCount'),
    url(r'^Dashboard/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/(?P<gid>\d+)/GetResStatus/$', dash_getDashResourceStatus, name='dash_getDashResourceStatus'),
    ###################################
    url(r'^WorkOrder/$',list_wo,name='list_wo'),

    url(r'^formset$',formset_view,name='formset_view'),
    url(r'^formset/remove/(?P<ids>\d+(?:,\d+)*)$',formset_bulk_deletion,name='formset_bulk_deletion'),
    url(r'^formset/remove/$',formset_bulk_deletion,name='formset_bulk_deletion'),
    url(r'^formsetcreate$',save_formset,name='save_formset'),
    url(r'^WorkOrder/create/$', wo_create, name='wo_create'),
    url(r'^WorkOrder/(?P<id>\d+)/update/$', wo_update, name='wo_update'),
    url(r'^WorkOrder/(?P<id>\d+)/cancel/$', wo_cancel, name='wo_cancel'),
    url(r'^WorkOrder/(?P<id>\d+)/delete/$', wo_delete, name='wo_delete'),

    url(r'^WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/(?P<wotype>\d+)/(?P<ordercol>\d+)/filter/(?P<ordertype>\d+)$', wo_filter, name='wo_filter'),


    url(r'^MiniWorkorder/$',list_miniWorkorder,name='list_miniWorkorder'),
    url(r'^MiniWorkorder/create/$', miniWorkorder_create, name='miniWorkorder_create'),
    url(r'^MiniWorkorder/(?P<id>\d+)/update/$', miniWorkorder_update, name='miniWorkorder_update'),
    url(r'^MiniWorkorder/(?P<id>\d+)/view/$', miniWorkorder_view, name='miniWorkorder_view'),

    url(r'^MiniWorkorder/(?P<id>\d+)/delete/$', miniWorkorder_delete, name='miniWorkorder_delete'),


    url(r'^WorkOrder/(?P<wid>\d+)/(?P<aid>\d+)/setAsset/$', wo_setAsset, name='wo_setAsset'),
    url(r'^WorkOrder/(?P<id>\d+)/deleteChildren$', wo_deleteChildren, name='wo_deleteChildren'),
    url(r'^WorkOrder/GetProblems$', wo_getProblem, name='wo_getProblem'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/HighPriority/$',woGetHighPriority,name='woGetHighPriority'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/OpenWorkOrder/$',woGetOpenWO,name='woGetOpenWO'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/CloseWorkOrder/$',woGetCloseWO,name='woGetCloseWO'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/OverdueWorkOrder/$',woGetOverdueWO,name='woGetOverdueWO'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/EM/$',showEM,name='showEM'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/taviz/$',showtaviz,name='showtaviz'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/tavaghof/$',showtavaghof,name='showtaviz'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/overdue/$',showmonghazi,name='showmonghazi'),
    url(r'WorkOrder/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/new/$',shownewwo,name='shownewwo'),
    url(r'^WorkOrder/ListCurrentWeek$', list_lastweek_wo, name='list_lastweek_wo'),
    url(r'^WorkOrder/ListCurrentMonth$', list_lastmonth_wo, name='list_lastmonth_wo'),
    url(r'^WorkOrder/ListCurrentDay$', list_lastday_wo, name='list_lastday_wo'),
    url(r'^WorkOrder/(?P<id>\d+)/WorkHour/$', wo_work_hour, name='wo_work_hour'),
    url(r'^WorkOrder/(?P<id>\d+)/updateEm/(?P<val>\d+)$', updateEm, name='updateEm'),
    url(r'^WorkOrder/(?P<searchStr>[-\w]+)/Search/$', wo_searchWorkOrderByTags, name='wo_searchWorkOrderByTags'),
    url(r'^WorkOrder/(?P<id>-?\d+)/getType/$', woTypes, name='woTypes'),
    url(r'^WorkOrder/(?P<id>-?\d+)/getGroup/$', woGroups, name='woGroups'),
    url(r'^WorkOrder/GetWos$', wo_getwos, name='wo_getwos'),
    url(r'^WorkOrder/(?P<id>-?\d+)/details$', wo_detail, name='wo_detail'),
    url(r'^WorkOrder/bulkEm/$', set_wo_to_em, name='set_wo_to_em'),
    url(r'^WorkOrder/bulkEm/(?P<ids>\d+(?:,\d+)*)$', set_wo_to_em, name='set_wo_to_em'),



    url(r'^SWorkOrder/$',list_swo,name='list_swo'),
    url(r'^SWorkOrder/create/$', swo_create, name='swo_create'),
    url(r'^SWorkOrder/(?P<id>\d+)/update/$', swo_update, name='swo_update'),
    url(r'^SWorkOrder/(?P<id>\d+)/delete/$', swo_delete, name='swo_delete'),

    url(r'^SWorkOrder/(?P<id>\d+)/deleteChildren$', swo_deleteChildren, name='swo_deleteChildren'),

    url(r'^SWorkOrder/(?P<id>\d+)/Running/$', SWOupdateRunning, name='SWOupdateRunning'),
    url(r'^SWorkOrder/(?P<wid>\d+)/(?P<aid>\d+)/setAsset/$', swo_setAsset, name='swo_setAsset'),
    url(r'^SWorkOrder/(?P<searchStr>[^/]+)/Search/$', swo_searchworkOrderByTags, name='swo_searchworkOrderByTags'),
    url(r'^SWorkOrder/(?P<id>\d+)/cancel/$', swo_cancel, name='swo_cancel'),
    url(r'^SWorkOrder/(?P<status>\d+)/swo_show_swo_by_type/$', swo_show_swo_by_type, name='swo_show_swo_by_type'),
    url(r'^SWorkOrder/(?P<status>\d+)/swo_show_swo_by_schedule_type/$', swo_show_swo_by_schedule_type, name='swo_show_swo_by_schedule_type'),


     url(r'^Task/$',list_task,name='list_task'),
     url(r'^Task/create/$', task_create, name='task_create'),
     # url(r'^Task/(?P<id>\d+)/create/$', task_create, name='task_create'),
     url(r'^Task/(?P<id>\d+)/delete/$', task_delete, name='task_delete'),
     url(r'^Task/(?P<woId>\d+)/listTask/$', js_list_task, name='js_list_task'),
     url(r'^Task/(?P<id>\d+)/update/$', task_update, name='task_update'),


     url(r'^Task/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/(?P<t1>[^/]+)/(?P<t2>[^/]+)/TaskWorkHour/$', getTaskWoHour, name='getTaskWoHour'),

     url(r'^TaskGroup/$',list_taskGroup,name='list_taskGroup'),
     url(r'^TaskGroup/(?P<assetId>\d+)/js/$',list_taskGroup_js,name='list_taskGroup_js'),
     url(r'^TaskGroup/create/$', taskGroup_create, name='taskGroup_create'),
     url(r'^TaskGroup/(?P<id>\d+)/delete/$', taskGroup_delete, name='taskGroup_delete'),
     url(r'^TaskGroup/(?P<id>\d+)/update/$', taskGroup_update, name='taskGroup_update'),
     url(r'^TaskGroup/(?P<tid>\d+)/(?P<woid>\d+)/register/$', registerTaskGroup, name='registerTaskGroup'),
     url(r'^TaskGroup/(?P<id>\d+)/Cancel/$', taskGroupCancel, name='taskGroupCancel'),
     url(r'^TaskGroup/(?P<str>\w+)/search/$', taskGroupSearch, name='taskGroupSearch'),

     url(r'^TaskTemplate/$',list_taskTemplate,name='list_taskTemplate'),
     url(r'^TaskTemplate/create/$', taskTemplate_create, name='taskTemplate_create'),
     url(r'^TaskTemplate/(?P<id>\d+)/delete/$', taskTemplate_delete, name='taskTemplate_delete'),
     url(r'^TaskTemplate/(?P<woId>\d+)/listTaskTemplate/$', js_list_taskTemplate, name='js_list_taskTemplate'),
     url(r'^TaskTemplate/(?P<id>\d+)/update/$', taskTemplate_update, name='taskTemplate_update'),

     url(r'^TaskGroupAssetCategory/$',list_taskGroupAssetCategory,name='list_taskGroupAssetCategory'),
     url(r'^TaskGroupAssetCategory/create/$', taskGroupAssetCategory_create, name='taskGroupAssetCategory_create'),
     url(r'^TaskGroupAssetCategory/(?P<id>\d+)/delete/$', taskGroupAssetCategory_delete, name='taskGroupAssetCategory_delete'),
     url(r'^TaskGroupAssetCategory/(?P<id>\d+)/update/$', taskGroupAssetCategory_update, name='taskGroupAssetCategory_update'),
     url(r'^TaskGroupAssetCategory/(?P<woId>\d+)/listTaskGroupAssetCategory/$', js_list_taskGroupAssetCategory, name='js_list_taskGroupAssetCategory'),

     url(r'^TaskGroupFile/$',list_taskGroupFile,name='list_taskGroupFile'),
     url(r'^TaskGroupFile/(?P<taskGroupFileId>\d+)/listTaskGroupFile/$', js_list_taskGroupFile, name='js_list_taskGroupFile'),
     url(r'^TaskGroupFile/(?P<Id>\d+)/basic-upload/$', TaskGroupBasicUploadView.as_view(), name='taskgroupbasic_upload'),


      url(r'^WoPart/$',list_woPart,name='list_woPart'),
      url(r'^WoPart/create/$', woPart_create, name='woPart_create'),
      url(r'^WoPart/(?P<id>\d+)/create/$', woPart_create, name='woPart_create'),
      url(r'^WoPart/(?P<id>\d+)/delete/$', woPart_delete, name='woPart_delete'),
      url(r'^WoPart/(?P<id>\d+)/update/$', woPart_update, name='woPart_update'),
      url(r'^WoPart/(?P<name>\w+)/search/$', woPart_Seach, name='woPart_Seach'),
      url(r'^WoPart/(?P<woId>\d+)/listWoPart/$', js_list_woPart, name='js_list_woPart'),
      url(r'^WoPart/GetParts$', wo_getParts, name='wo_getParts'),
      url(r'^WoPart/GetStockParts$', wo_getStockParts, name='wo_getStockParts'),
      url(r'^WoPart/(?P<id>\d+)/GetPartStock/$', wP_getPartStock, name='wP_getPartStock'),

      url(r'^WoMeter/$',list_woMeter,name='list_woMeter'),
      url(r'^WoMeter/(?P<id>\d+)/create/$', woMeter_create, name='woMeter_create'),
      url(r'^WoMeter/create/$', woMeter_create, name='woMeter_create'),
      url(r'^WoMeter/(?P<id>\d+)/delete/$', woMeter_delete, name='woMeter_delete'),
      url(r'^WoMeter/(?P<id>\d+)/update/$', woMeter_update, name='woMeter_update'),
      url(r'^WoMeter/(?P<woId>\d+)/listWoMeter/$', js_list_woMeter, name='js_list_woMeter'),

      url(r'^WoPert/$',list_woPert,name='list_woPert'),
      url(r'^WoPert/create/$', woPert_create, name='woPert_create'),
      url(r'^WoPert/(?P<id>\d+)/create/$', woPert_create, name='woPert_create'),
      url(r'^WoPert/(?P<id>\d+)/delete/$', woPert_delete, name='woPert_delete'),
      url(r'^WoPert/(?P<id>\d+)/update/$', woPert_update, name='woPert_update'),
      url(r'^WoPert/(?P<woId>\d+)/listWoPert/$', js_list_woPert, name='js_list_woPert'),

      url(r'^WoMisc/$',list_woMisc,name='list_woMisc'),
      url(r'^WoMisc/create/$', woMisc_create, name='woMisc_create'),
      url(r'^WoMisc/(?P<id>\d+)/delete/$', woMisc_delete, name='woMisc_delete'),
      url(r'^WoMisc/(?P<id>\d+)/update/$', woMisc_update, name='woMisc_update'),
      url(r'^WoMisc/(?P<woId>\d+)/listWoMisc/$', js_list_woMisc, name='js_list_woMisc'),


      url(r'^WoNotify/$',list_woNotify,name='list_woNotify'),
      url(r'^WoNotify/create/$', woNotify_create, name='woNotify_create'),
      url(r'^WoNotify/(?P<id>\d+)/delete/$', woNotify_delete, name='woNotify_delete'),
      url(r'^WoNotify/(?P<id>\d+)/update/$', woNotify_update, name='woNotify_update'),
      url(r'^WoNotify/(?P<woId>\d+)/listWoNotify/$', js_list_woNotify, name='js_list_woNotify'),


       url(r'^WoFile/(?P<woId>\d+)/listWoFile/$', js_list_woFile, name='js_list_woFile'),
       url(r'^WoFile/(?P<Id>\d+)/basic-upload/$', WorkOrderUploadView.as_view(), name='workorder_upload'),

       url(r'^WoLog/(?P<woId>\d+)/listWoLog/$', js_list_woLog, name='js_list_woLog'),


       url(r'^Schedule/$',list_schedule,name='list_schedule'),
       url(r'^Schedule/create/$', schedule_create, name='schedule_create'),
       url(r'^Schedule/(?P<id>\d+)/delete/$', schedule_delete, name='schedule_delete'),
       url(r'^Schedule/(?P<id>\d+)/update/$', schedule_update, name='schedule_update'),
       url(r'^Schedule/(?P<woId>\d+)/listSchedule/$', js_list_schedule, name='js_list_schedule'),


        url(r'^Asset/$',list_asset,name='list_asset'),
        url(r'^Asset/DASH/$',list_asset_dash,name='list_asset_dash'),
        url(r'^Asset/Location/$',list_asset_location,name='list_asset_location'),
        url(r'^Asset/Machine/$',list_asset_machine,name='list_asset_machine'),
        url(r'^Asset/Tool/$',list_asset_tool,name='list_asset_tool'),
        url(r'^Asset/Types/(?P<ids>\d+(?:,\d+)*)$',show_asset_types,name='show_asset_types'),
        url(r'^Asset/Update_Types/(?P<ids>\d+(?:,\d+)*)/(?P<cat>\d+)$',asset_type_update,name='asset_type_update'),
        #url(r'^Asset/Location/$',list_location,name='list_location'),
        #url(r'^Asset/Machine/$',list_machine,name='list_machine'),
        #url(r'^Asset/Tool/$',list_tool,name='list_tool'),
        url(r'^Asset/GetAssetType/$',asset_type_selector,name='asset_type_selector'),
        # url(r'^Asset/Category2/$', get_assetCategoryMain, name='get_assetCategoryMain'),
        # url(r'^Asset/Category2/(?P<ids>\d+(?:,\d+)*)$', get_assetCategoryMain, name='get_assetCategoryMain'),
        url(r'^Asset/Location/create/$', asset_create_location, name='asset_create_location'),
        url(r'^Asset/(?P<kvm>[\w\s]+)/(?P<searchStr>[-\w]+)/Search/$', asset_search, name='asset_search'),

        url(r'^Asset/Machine/create/$', asset_create_machine, name='asset_create_machine'),
        url(r'^Asset/Tool/create/$', asset_create_tool, name='asset_create_tool'),
        url(r'^Asset/(?P<id>\d+)/delete/$', asset_delete, name='asset_delete'),
        url(r'^Asset/(?P<id>\d+)/update/$', asset_update, name='asset_update'),

        url(r'^Asset/Category/$', get_assetCategory, name='get_assetCategory'),
        url(r'^Asset/Category2/$', get_assetCategoryMain, name='get_assetCategoryMain'),
        url(r'^Asset/Category2/(?P<ids>\d+(?:,\d+)*)$', get_assetCategoryMain, name='get_assetCategoryMain'),
        url(r'^Asset/Location/Category$', get_location_by_category, name='get_location_by_category'),

        url(r'^Asset/(?P<id>\d+)/show_Asset_status/$', show_Asset_status, name='show_Asset_status'),
        url(r'^Asset/(?P<id>\d+)/MTTR/$', asset_mttr, name='asset_mttr'),
        url(r'^Asset/(?P<id>\d+)/MTBF/$', asset_mtbf, name='asset_mtbf'),
        url(r'^Asset/(?P<id>\d+)/WOStatus/$', asset_status, name='asset_status'),
        url(r'^Asset/(?P<id>\d+)/GetAssetOfflineStatus/$', asset_offline_status, name='asset_offline_status'),
        url(r'^Asset/(?P<id>\d+)/Cancel/$', assetCancel, name='assetCancel'),


        url(r'^AssetWaranty/$',list_assetWaranty,name='list_assetWaranty'),
        url(r'^AssetWaranty/create/$', assetWaranty_create, name='assetWaranty_create'),
        url(r'^AssetWaranty/(?P<id>\d+)/delete/$', assetWaranty_delete, name='assetWaranty_delete'),
        url(r'^AssetWaranty/(?P<id>\d+)/update/$', assetWaranty_update, name='assetWaranty_update'),
        url(r'^AssetWaranty/(?P<woId>\d+)/listAssetWaranty/$', js_list_assetWaranty, name='js_list_assetWaranty'),

        url(r'^AssetMeter/$',list_assetMeter,name='list_assetMeter'),
        url(r'^AssetMeter/create/$', assetMeter_create, name='assetMeter_create'),
        url(r'^AssetMeter/(?P<id>\d+)/create/$', assetMeter_create, name='assetMeter_create'),
        url(r'^AssetMeter/(?P<id>\d+)/delete/$', assetMeter_delete, name='assetMeter_delete'),
        url(r'^AssetMeter/(?P<id>\d+)/update/$', assetMeter_update, name='assetMeter_update'),
        url(r'^AssetMeter/(?P<woId>\d+)/listAssetMeter/$', js_list_assetMeter, name='js_list_assetMeter'),


        url(r'^AssetBusiness/$',list_assetBusiness,name='list_assetBusiness'),
        url(r'^AssetBusiness/create/$', assetBusiness_create, name='assetBusiness_create'),
        url(r'^AssetBusiness/(?P<id>\d+)/delete/$', assetBusiness_delete, name='assetBusiness_delete'),
        url(r'^AssetBusiness/(?P<id>\d+)/update/$', assetBusiness_update, name='assetBusiness_update'),
        url(r'^AssetBusiness/(?P<woId>\d+)/listAssetBusiness/$', js_list_assetBusiness, name='js_list_assetBusiness'),

        url(r'^AssetPurchase/$',list_assetPurchase,name='list_assetPurchase'),
        url(r'^AssetPurchase/create/$', assetPurchase_create, name='assetPurchase_create'),
        url(r'^AssetPurchase/(?P<id>\d+)/delete/$', assetPurchase_delete, name='assetPurchase_delete'),
        url(r'^AssetPurchase/(?P<id>\d+)/update/$', assetPurchase_update, name='assetPurchase_update'),
        url(r'^AssetPurchase/(?P<woId>\d+)/listAssetPurchase/$', js_list_assetPurchase, name='js_list_assetPurchase'),



        url(r'^AssetPart/$',list_assetPart,name='list_assetPart'),
        url(r'^AssetPart/create/$', assetPart_create, name='assetPart_create'),
        url(r'^AssetPart/(?P<id>\d+)/delete/$', assetPart_delete, name='assetPart_delete'),
        url(r'^AssetPart/(?P<id>\d+)/update/$', assetPart_update, name='assetPart_update'),
        url(r'^AssetPart/(?P<woId>\d+)/listAssetPart/$', js_list_assetPart, name='js_list_assetPart'),


        url(r'^BOMGroupPart/create/$', bomGroupPart_create, name='bomGroupPart_create'),
        url(r'^BOMGroupPart/(?P<id>\d+)/delete/$', bomGroupPart_delete, name='bomGroupPart_delete'),
        url(r'^BOMGroupPart/(?P<id>\d+)/update/$', bomGroupPart_update, name='bomGroupPart_update'),
        url(r'^BOMGroupPart/(?P<woId>\d+)/listBOMGroupPart/$', js_list_bomGroupPart, name='js_list_bomGroupPart'),

        url(r'^BOMGroupAsset/create/$', bomGroupAsset_create, name='bomGroupAsset_create'),
        url(r'^BOMGroupAsset/(?P<id>\d+)/delete/$', bomGroupAsset_delete, name='bomGroupAsset_delete'),
        url(r'^BOMGroupAsset/(?P<id>\d+)/update/$', bomGroupAsset_update, name='bomGroupAsset_update'),
        url(r'^BOMGroupAsset/(?P<woId>\d+)/listBOMGroupAsset/$', js_list_bomGroupAsset, name='js_list_bomGroupAsset'),


        url(r'^AssetEvent/$',list_assetEvent,name='list_assetEvent'),
        url(r'^AssetEvent/create/$', assetEvent_create, name='assetEvent_create'),
        url(r'^AssetEvent/(?P<id>\d+)/delete/$', assetEvent_delete, name='assetEvent_delete'),
        url(r'^AssetEvent/(?P<id>\d+)/update/$', assetEvent_update, name='assetEvent_update'),
        url(r'^AssetEvent/(?P<woId>\d+)/listAssetEvent/$', js_list_assetEvent, name='js_list_assetEvent'),


        url(r'^AssetLife/$',list_assetLife,name='list_assetLife'),
        url(r'^AssetLife/(?P<assetId>\d+)/create/$', assetLife_create, name='assetLife_create'),
        url(r'^AssetLife/(?P<assetId>\d+)/eval/$', findLastOpenAssetLife, name='findLastOpenAssetLife'),
        url(r'^AssetLife/create/$', assetLife_create, name='assetLife_create'),
        url(r'^AssetLife/(?P<id>\d+)/delete/$', assetLife_delete, name='assetLife_delete'),
        url(r'^AssetLife/(?P<id>\d+)/update/$', assetLife_update, name='assetLife_update'),
        url(r'^AssetLife/(?P<woId>\d+)/listAssetLife/$', js_list_assetLife, name='js_list_assetLife'),



        url(r'^AssetUser/$',list_assetUser,name='list_assetUser'),
        url(r'^AssetUser/create/$', assetUser_create, name='assetUser_create'),
        url(r'^AssetUser/(?P<id>\d+)/delete/$', assetUser_delete, name='assetUser_delete'),
        url(r'^AssetUser/(?P<id>\d+)/update/$', assetUser_update, name='assetUser_update'),
        url(r'^AssetUser/(?P<woId>\d+)/listAssetUser/$', js_list_assetUser, name='js_list_assetUser'),


        url(r'^AssetFile/(?P<woId>\d+)/listAssetFile/$', js_list_assetFile, name='js_list_assetFile'),
        url(r'^AssetFile/(?P<Id>\d+)/basic-upload/$', AssetFileUploadView.as_view(), name='asset_upload'),

         url(r'^AssetCategory/$',list_assetCategory,name='list_assetCategory'),
         url(r'^AssetCategory/create/$', assetCategory_create, name='assetCategory_create'),
         url(r'^AssetCategory/(?P<id>\d+)/delete/$', assetCategory_delete, name='assetCategory_delete'),
         url(r'^AssetCategory/(?P<id>\d+)/update/$', assetCategory_update, name='assetCategory_update'),

         url(r'^MachineCategory/$',list_machineCategory,name='list_machineCategory'),
         url(r'^MachineCategory/create/$', machineCategory_create, name='machineCategory_create'),
         url(r'^MachineCategory/(?P<id>\d+)/delete/$', machineCategory_delete, name='machineCategory_delete'),
         url(r'^MachineCategory/(?P<id>\d+)/update/$', machineCategory_update, name='machineCategory_update'),

        url(r'^Part/$',list_part,name='list_part'),
        url(r'^Part/create/$', part_create, name='part_create'),
        url(r'^Part/create2/$', part_create2, name='part_create2'),#for wopart modal form dynamic part creation
        url(r'^Part/(?P<id>\d+)/delete/$', part_delete, name='part_delete'),
        url(r'^Part/(?P<id>\d+)/update/$', part_update, name='part_update'),
        url(r'^Part/(?P<searchStr>[-\w]+)/Search/$', part_searchPart, name='part_searchPart'),
        url(r'^Part/(?P<id>\d+)/Cancel/$', partCancel, name='partCancel'),
        url(r'^Part/(?P<id>\d+)/InventorySum/$', inventorySum, name='inventorySum'),
        url(r'^Part/(?P<id>\d+)/InventoryLevel/$', inventoryLevel, name='inventoryLevel'),
        url(r'^Part/(?P<id>\d+)/GetPartUsage/$', partUsage, name='partUsage'),
        url(r'^Part/(?P<id>\d+)/(?P<num>\d+)/GetConsumes/$', getPartConsumedItem, name='get_part_consumed_item'),
        url(r'^Part/(?P<id>\d+)/(?P<num>\d+)/GetPurchases/$', getPartPurchasedItem, name='get_part_purchaseditem'),

        url(r'^PartStock/$',list_partStock,name='list_partStock'),
        url(r'^PartStock/create/$', partStock_create, name='partStock_create'),
        url(r'^PartStock/(?P<id>\d+)/delete/$', partStock_delete, name='partStock_delete'),
        url(r'^PartStock/(?P<id>\d+)/update/$', partStock_update, name='partStock_update'),
        url(r'^PartStock/(?P<woId>\d+)/listPartStock/$', js_list_partStock, name='js_list_partStock'),

        url(r'^PartLocation/$',list_partLocation,name='list_partLocation'),
        url(r'^PartLocation/create/$', partLocation_create, name='partLocation_create'),
        url(r'^PartLocation/(?P<id>\d+)/delete/$', partLocation_delete, name='partLocation_delete'),
        url(r'^PartLocation/(?P<id>\d+)/update/$', partLocation_update, name='partLocation_update'),
        url(r'^PartLocation/(?P<woId>\d+)/listPartLocation/$', js_list_partLocation, name='js_list_partLocation'),

        url(r'^PartUser/$',list_partUser,name='list_partUser'),
        url(r'^PartUser/create/$', partUser_create, name='partUser_create'),
        url(r'^PartUser/(?P<id>\d+)/delete/$', partUser_delete, name='partUser_delete'),
        url(r'^PartUser/(?P<id>\d+)/update/$', partUser_update, name='partUser_update'),
        url(r'^PartUser/(?P<woId>\d+)/listPartUser/$', js_list_partUser, name='js_list_partUser'),

        url(r'^PartWaranty/$',list_partWaranty,name='list_partWaranty'),
        url(r'^PartWaranty/create/$', partWaranty_create, name='partWaranty_create'),
        url(r'^PartWaranty/(?P<id>\d+)/delete/$', partWaranty_delete, name='partWaranty_delete'),
        url(r'^PartWaranty/(?P<id>\d+)/update/$', partWaranty_update, name='partWaranty_update'),
        url(r'^PartWaranty/(?P<woId>\d+)/listPartWaranty/$', js_list_partWaranty, name='js_list_partWaranty'),
        url(r'^PartBusiness/$',list_partBusiness,name='list_partBusiness'),
        url(r'^PartBusiness/create/$', partBusiness_create, name='partBusiness_create'),
        url(r'^PartBusiness/(?P<id>\d+)/delete/$', partBusiness_delete, name='partBusiness_delete'),
        url(r'^PartBusiness/(?P<id>\d+)/update/$', partBusiness_update, name='partBusiness_update'),
        url(r'^PartBusiness/(?P<woId>\d+)/listPartBusiness/$', js_list_partBusiness, name='js_list_partBusiness'),

        url(r'^PartPurchase/$',list_partPurchase,name='list_partPurchase'),
        url(r'^PartPurchase/create/$', partPurchase_create, name='partPurchase_create'),
        url(r'^PartPurchase/(?P<id>\d+)/delete/$', partPurchase_delete, name='partPurchase_delete'),
        url(r'^PartPurchase/(?P<id>\d+)/update/$', partPurchase_update, name='partPurchase_update'),
        url(r'^PartPurchase/(?P<woId>\d+)/listPartPurchase/$', js_list_partPurchase, name='js_list_partPurchase'),

        url(r'^PartFile/$',list_partFile,name='list_partFile'),
        url(r'^PartFile/create/$', partFile_create, name='partFile_create'),
        url(r'^PartFile/(?P<id>\d+)/delete/$', partFile_delete, name='partFile_delete'),
        url(r'^PartFile/(?P<id>\d+)/update/$', partFile_update, name='partFile_update'),
        url(r'^PartFile/(?P<woId>\d+)/listPartFile/$', js_list_partFile, name='js_list_partFile'),
        url(r'^PartFile/(?P<Id>\d+)/basic-upload/$', PartFileUploadView.as_view(), name='part_upload'),

        url(r'^Stock/$',list_stock,name='list_stock'),
        url(r'^Stock/create/$', stock_create, name='stock_create'),
        url(r'^Stock/create2/$', stock_create2, name='stock_create2'),#for wopart modal stock creation
        url(r'^Stock/(?P<id>\d+)/delete/$', stock_delete, name='stock_delete'),
        url(r'^Stock/(?P<id>\d+)/update/$', stock_update, name='stock_update'),
        url(r'^Stock/(?P<woId>\d+)/listStock/$', js_list_stock, name='js_list_stock'),
        url(r'^Stock/listStockModal/$', js_list_modal_stock, name='js_list_modal_stock'),
        url(r'^Stock/LowItem/$', list_lowItemStock, name='list_lowItemStock'),
        url(r'^Stock/LowItemDetails/$', get_lowItemStock, name='get_lowItemStock'),
        url(r'^Stock/ListAllItemDetails/$', js_list_all_stock, name='js_list_all_stock'),
        url(r'^Stock/(?P<locationId>\d+)/ListGroupedStock/$', groupByStockLocation, name='group_by_stock_location'),
        url(r'^Stock/(?P<stockId>\d+)/(?P<num>\d+)/GetConsumes/$', getConsumedItem, name='get_consumed_item'),
        url(r'^Stock/(?P<stockId>\d+)/(?P<num>\d+)/GetPurchases/$', getPurchasedItem, name='get_purchaseditem'),
        url(r'^Stock/(?P<searchStr>[-\w]+)/Search/$', stockSearch, name='stockSearch'),
        url(r'^Stock/(?P<searchStr>[-\w]+)/Search2/$', stockSearch2, name='stockSearch2'),


         url(r'^Business/$',list_business,name='list_business'),
         url(r'^Business/create/$', business_create, name='business_create'),
         url(r'^Business/(?P<id>\d+)/delete/$', business_delete, name='business_delete'),
         url(r'^Business/(?P<id>\d+)/update/$', business_update, name='business_update'),
         url(r'^Business/(?P<id>\d+)/Cancel/$', businessCancel, name='businessCancel'),

         url(r'^BOMGroup/$',list_bomgroup,name='list_bomgroup'),
         url(r'^BOMGroup/create/$', bomgroup_create, name='bomgroup_create'),
         url(r'^BOMGroup/(?P<id>\d+)/delete/$', bomgroup_delete, name='bomgroup_delete'),
         url(r'^BOMGroup/(?P<id>\d+)/update/$', bomgroup_update, name='bomgroup_update'),
         # url(r'^BOMGroup/(?P<id>\d+)/Cancel/$', bomgroupCancel, name='bomgroupCancel'),

          url(r'^Event/$',list_event,name='list_event'),
          url(r'^Event/create/$', event_create, name='event_create'),
          url(r'^Event/(?P<id>\d+)/delete/$', event_delete, name='event_delete'),
          url(r'^Event/(?P<id>\d+)/update/$', event_update, name='event_update'),

          url(r'^MaintenanceType/$',list_maintenanceType,name='list_maintenanceType'),
          url(r'^MaintenanceType/create/$', maintenanceType_create, name='maintenanceType_create'),
          url(r'^MaintenanceType/(?P<id>\d+)/delete/$', maintenanceType_delete, name='maintenanceType_delete'),
          url(r'^MaintenanceType/(?P<id>\d+)/update/$', maintenanceType_update, name='maintenanceType_update'),
          url(r'^Attendance/$',list_attendance,name='list_attendance'),
          url(r'^Attendance/Mass/$',mass_create,name='mass_create'),
          url(r'^Attendance/$',list_attendance,name='list_attendance'),
          url(r'^Attendance/create/$', attendance_create, name='attendance_create'),
          url(r'^Attendance/batchcreate/$', attendance_batch_create, name='attendance_batch_create'),
          url(r'^Attendance/(?P<id>\d+)/delete/$', attendance_delete, name='attendance_delete'),
          url(r'^Attendance/(?P<id>\d+)/update/$', attendance_update, name='attendance_update'),
          url(r'^Attendance/(?P<gid>\d+)/batchlist/$', attendanceGetUser, name='attendanceGetUser'),


          url(r'^BusinessFile/$',list_businessFile,name='list_businessFile'),
          url(r'^BusinessFile/create/$', businessFile_create, name='businessFile_create'),
          url(r'^BusinessFile/(?P<id>\d+)/delete/$', businessFile_delete, name='businessFile_delete'),
          url(r'^BusinessFile/(?P<id>\d+)/update/$', businessFile_update, name='businessFile_update'),
          url(r'^BusinessFile/(?P<woId>\d+)/listBusinessFile/$', js_list_businessFile, name='js_list_businessFile'),
          url(r'^BusinessFile/(?P<Id>\d+)/basic-upload/$', BusinessFileUploadView.as_view(), name='business_upload'),

          url(r'^BusinessAsset/$',list_businessAsset,name='list_businessAsset'),
          url(r'^BusinessAsset/create/$', businessAsset_create, name='businessAsset_create'),
          url(r'^BusinessAsset/(?P<id>\d+)/delete/$', businessAsset_delete, name='businessAsset_delete'),
          url(r'^BusinessAsset/(?P<id>\d+)/update/$', businessAsset_update, name='businessAsset_update'),
          url(r'^BusinessAsset/(?P<woId>\d+)/listBusinessAsset/$', js_list_businessAsset, name='js_list_businessAsset'),

          url(r'^BusinessPart/$',list_businessPart,name='list_businessPart'),
          url(r'^BusinessPart/create/$', businessPart_create, name='businessPart_create'),
          url(r'^BusinessPart/(?P<pid>\d+)/create/$', businessPart_create, name='businessPart_create'),
          url(r'^BusinessPart/(?P<id>\d+)/delete/$', businessPart_delete, name='businessPart_delete'),
          url(r'^BusinessPart/(?P<id>\d+)/update/$', businessPart_update, name='businessPart_update'),
          url(r'^BusinessPart/(?P<woId>\d+)/listBusinessPart/$', js_list_businessPart, name='js_list_businessPart'),

           url(r'^Mail/$',list_mail,name='list_mail'),
           url(r'^Mail/create/$', mail_create, name='mail_create'),
           url(r'^Mail/(?P<id>\d+)/delete/$', mail_delete, name='mail_delete'),
           url(r'^Mail/(?P<id>\d+)/update/$', mail_update, name='mail_update'),
           url(r'^Mail/Sent/$', list_sentmail, name='list_sentmail'),
           url(r'^Mail/Status/$', list_unread_mail, name='list_unread_mail'),
           url(r'^Mail/System/$', list_sysmail, name='list_sysmail'),


           url(r'^Project/$',list_project,name='list_project'),
           url(r'^Project/create/$', project_create, name='project_create'),
           url(r'^Project/(?P<id>\d+)/delete/$', project_delete, name='project_delete'),

           url(r'^Project/(?P<id>\d+)/update/$', project_update, name='project_update'),
           url(r'^Project/(?P<searchStr>[-\w]+)/Search/$', projectSearch, name='projectSearch'),
           url(r'^Project/(?P<id>\d+)/brief/$', projectInBrief, name='projectInBrief'),
           url(r'^Project/(?P<id>\d+)/Cancel/$', projectCancel, name='projectCancel'),
           url(r'^ProjectScheduled/(?P<woId>\d+)/listProjectScheduled/$', js_list_projectScheduled, name='js_list_projectScheduled'),
           url(r'^ProjectWo/(?P<woId>\d+)/listProjectWo/$', js_list_projectWo, name='js_list_projectWo'),

           url(r'^ProjectUser/$',list_projectUser,name='list_projectUser'),
           url(r'^ProjectUser/create/$', projectUser_create, name='projectUser_create'),

           url(r'^ProjectUser/(?P<id>\d+)/delete/$', projectUser_delete, name='projectUser_delete'),
           url(r'^ProjectUser/(?P<id>\d+)/update/$', projectUser_update, name='projectUser_update'),
           url(r'^ProjectUser/(?P<woId>\d+)/listProjectUser/$', js_list_projectUser, name='js_list_projectUser'),

           url(r'^ProjectFile/$',list_projectFile,name='list_projectFile'),
           url(r'^ProjectFile/create/$', projectFile_create, name='projectFile_create'),
           url(r'^ProjectFile/(?P<id>\d+)/delete/$', projectFile_delete, name='projectFile_delete'),
           url(r'^ProjectFile/(?P<id>\d+)/update/$', projectFile_update, name='projectFile_update'),
           url(r'^ProjectFile/(?P<woId>\d+)/listProjectFile/$', js_list_projectFile, name='js_list_projectFile'),
           url(r'^ProjectFile/(?P<Id>\d+)/basic-upload/$', ProjectFileUploadView.as_view(), name='project_upload'),

           url(r'^SettingPage/$',list_settings,name='list_settings'),
           url(r'^SettingPage/WOProblem/listWoProblem$',js_list_woProblem,name='js_list_woProblem'),
           url(r'^SettingPage/WOProblem/create/$', woProblem_create, name='woProblem_create'),
           url(r'^SettingPage/WOProblem/(?P<id>\d+)/delete/$', woProblem_delete, name='woProblem_delete'),
           url(r'^SettingPage/WOProblem/(?P<id>\d+)/update/$', woProblem_update, name='woProblem_update'),
           url(r'^SettingPage/WOStop/listWoStop$',js_list_woStop,name='js_list_woStop'),
           url(r'^SettingPage/WOStop/create/$', woStop_create, name='woStop_create'),
           url(r'^SettingPage/WOStop/(?P<id>\d+)/delete/$', woStop_delete, name='woStop_delete'),
           url(r'^SettingPage/WOStop/(?P<id>\d+)/update/$', woStop_update, name='woStop_update'),

           url(r'^SettingPage/WOPert/listWoPert$',js_list_workorderPert,name='js_list_workorderPert'),
           url(r'^SettingPage/WOPert/create/$', workorderPert_create, name='workorderPert_create'),
           url(r'^SettingPage/WOPert/(?P<id>\d+)/delete/$', workorderPert_delete, name='workorderPert_delete'),
           url(r'^SettingPage/WOPert/(?P<id>\d+)/update/$', workorderPert_update, name='workorderPert_update'),

           url(r'^SettingPage/WOCause/listWoCause$',js_list_woCause,name='js_list_woCause'),
           url(r'^SettingPage/OfflineStatus/listOfflineStatus$',js_list_offlineStatus,name='js_list_offlineStatus'),
           url(r'^SettingPage/OfflineStatus/create/$', offlineStatus_create, name='offlineStatus_create'),
           url(r'^SettingPage/OfflineStatus/(?P<id>\d+)/delete/$', offlineStatus_delete, name='offlineStatus_delete'),
           url(r'^SettingPage/OfflineStatus/(?P<id>\d+)/update/$', offlineStatus_update, name='offlineStatus_update'),
           url(r'^SettingPage/WOCause/listWoCause$',js_list_woCause,name='js_list_woCause'),
           url(r'^SettingPage/WOCause/create/$', woCause_create, name='woCause_create'),
           url(r'^SettingPage/WOCause/(?P<id>\d+)/delete/$', woCause_delete, name='woCause_delete'),
           url(r'^SettingPage/WOCause/(?P<id>\d+)/update/$', woCause_update, name='woCause_update'),
           url(r'^SettingPage/WOAction/listWoAction$',js_list_woAction,name='js_list_woAction'),
           url(r'^SettingPage/WOAction/create/$', woAction_create, name='woAction_create'),
           url(r'^SettingPage/WOAction/(?P<id>\d+)/delete/$', woAction_delete, name='woAction_delete'),
           url(r'^SettingPage/WOAction/(?P<id>\d+)/update/$', woAction_update, name='woAction_update'),
           url(r'^SettingPage/EquipCost/listEquipCost$',js_list_equipCost,name='js_list_equipCost'),
           url(r'^SettingPage/EquipCost/create/$', equipCost_create, name='equipCost_create'),
           url(r'^SettingPage/EquipCost/(?P<id>\d+)/delete/$', equipCost_delete, name='equipCost_delete'),
           url(r'^SettingPage/EquipCost/(?P<id>\d+)/update/$', equipCost_update, name='equipCost_update'),
           url(r'^SettingPage/UserGroup/listUserGroup$',js_list_userGroup2,name='js_list_userGroup2'),
           url(r'^SettingPage/UserGroup/create/$', userGroup_create, name='userGroup_create'),
           url(r'^SettingPage/UserGroup/(?P<id>\d+)/delete/$', userGroup_delete, name='userGroup_delete'),
           url(r'^SettingPage/UserGroup/(?P<id>\d+)/update/$', userGroup_update, name='userGroup_update'),


           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetRequestedWo/$', GetRequestedWo, name='GetRequestedWo'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetWoReqNum/$', GetWoReqNum, name='GetWoReqNum'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetWoPartNum/$', GetWoPartNum, name='GetWoPartNum'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetStopNum/$', GeStopNum, name='GeStopNum'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetMTTR/$', GetMTTR, name='GetMTTR'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetMiscCost/$', GetMiscCost, name='GetMiscCost'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetHighPriorityWo/$', GetHighPriorityWO, name='GetHighPriorityWO'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetOpenWoReqNum/$', GetOpenWoReqNum, name='GetOpenWoReqNum'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetCloseWoReqNum/$', GetCloseWoReqNum, name='GetCloseWoReqNum'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetOverdueWoReqNum/$', GetOverdueWoReqNum, name='GetOverdueWoReqNum'),
           url(r'^Summery/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)/GetEmCount/$', GetEmCount, name='GetEmCount'),
           url(r'^Summery/GetLowItemStock/$', GetLowItemStock, name='GetLowItemStock'),




           url(r'^User/$',list_user,name='list_user'),
           url(r'^User/create/$', user_create, name='user_create'),
           url(r'^User/(?P<id>\d+)/update/$', user_update, name='user_update'),
           url(r'^User/(?P<name>[-\w]+)/Search/$', searchUser, name='searchUser'),
           url(r'^User/(?P<id>\d+)/delete/$', user_delete, name='user_delete'),
           url(r'^User/(?P<UserId>\d+)/eval/$', changeUserStatus, name='changeUserStatus'),
           url(r'^User/(?P<statusCode>\d+)/listUser/$', listUser, name='listUser'),
           url(r'^User/listActiveUser/$', list_active_user, name='list_active_user'),
           url(r'^User/listInActiveUser/$', list_inactive_user, name='list_inactive_user'),
           url(r'^User/listAllUser/$', list_all_user, name='list_all_user'),
           url(r'^User/profileImage$', views.UserProfileImageUploadView.as_view(), name='user_profile_image_upload'),
           url(r'^User/(?P<id>\d+)/DashDetails$', getUserDashbordSum, name='getUserDashbordSum'),
           url(r'^User/(?P<id>\d+)/Cancel/$', userCancel, name='userCancel'),

           url(r'^UserGroups/(?P<woId>\d+)/listUserGroups/$', js_list_userGroup, name='js_list_userGroup'),
           url(r'^UserGroups/(?P<userId>\d+)/(?P<groupId>\d+)/updateStatus/$', update_usergroup, name='update_usergroup'),
           url(r'^UserFile/(?P<id>\d+)/ListUserFile$',js_list_userFile,name='js_list_userFile'),
           # url(r'^UserFile/create/$', userFile_create, name='userFile_create'),
           # url(r'^UserFile/(?P<id>\d+)/delete/$', userFile_delete, name='userFile_delete'),
           # url(r'^UserFile/(?P<id>\d+)/update/$', userFile_update, name='userFile_update'),
           # url(r'^UserFile/(?P<id>\d+)/ListUserFile/$', js_list_userFile, name='js_list_userFile'),
           # url(r'^UserFile/(?P<Id>\d+)/basic-upload/$', UserFileUploadView.as_view(), name='user_upload'),
           url(r'^UserFile/(?P<Id>\d+)/basic-upload/$', UserFileUploadView.as_view(), name='user_upload'),

           url(r'^UserCertification/(?P<woId>\d+)/ListUserCert$',js_list_userCertification,name='js_list_userCertification'),
           url(r'^UserCertification/create/$', userCertification_create, name='userCertification_create'),
           url(r'^UserCertification/(?P<id>\d+)/delete/$', userCertification_delete, name='userCertification_delete'),
           url(r'^UserCertification/(?P<id>\d+)/update/$', userCertification_update, name='userCertification_update'),
           url(r'^UserCertification/(?P<woId>\d+)/listUserCertification/$', js_list_userCertification, name='js_list_userCertification'),


           # url(r'^AdSet/',list_a123,name='list_a123'),
           # url(r'^AdminSetting/create/$', adminSetting_create, name='adminSetting_create'),
           # url(r'^AdminSetting/(?P<id>\d+)/delete/$', adminSetting_delete, name='adminSetting_delete'),
           # url(r'^AdminSetting/(?P<id>\d+)/update/$', adminSetting_update, name='adminSetting_update'),
           # url(r'^AdminSetting/(?P<woId>\d+)/listUserCertification/$', js_list_adminSetting, name='js_list_adminSetting'),


           url(r'^UserLog/(?P<woId>\d+)/ListUserLog$',js_list_userLog,name='js_list_userLog'),
           url(r'^Report/$',list_report,name='list_report'),
           url(r'^Report/create/$', report_create, name='report_create'),
           url(r'^Report/(?P<repType>\d+)/create/$', simpleReport_create, name='simpleReport_create'),
           url(r'^Report/(?P<repType>\d+)/update/$', simpleReport_update, name='simpleReport_update'),
           url(r'^Report/(?P<lId>\d+)/Broker/$', simpleReportBroker, name='simpleReportBroker'),
           url(r'^Report/(?P<id>-?\d+)/FilterCategory/$', FilterReportCategory, name='FilterReportCategory'),
           url(r'^Report/(?P<str>[-\w]+)/reportSearch/$', reportSearch, name='reportSearch'),
           url(r'^Report/(?P<id>\d+)/fav_report/$', make_favorits_report, name='make_favorits_report'),
           url(r'^Report/(?P<id>\d+)/show_fav_reports/$', show_fav_reports, name='show_fav_reports'),
           url(r'^Calendar/$',list_calendar,name='list_calendar'),
           url(r'^Calendar/Update/(?P<mtId>-?\d+)/(?P<gId>-?\d+)/(?P<startHijri>[^/]+)/(?P<endHijri>[^/]+)$',display_calendar,name='display_calendar'),
           #api_view
           url(r'^api/v1/wos/$',workorder_collection, name='workorder_collection'),
           url(r'^api/v1/login/$',user_login, name='user_login'),













]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
