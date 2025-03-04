import requests as rqt
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
def send_confirm_wtf(next_user,company):
    #next_user is sys_user
    #company is workorderpart
    url = "https://app.wallmessage.com/api/sendMessage"
     
    if(next_user.tel1):
              
                payload={
                "appkey": "78dba514-1a21-478e-8484-aecd14b198b7",
                "authkey": "ipnKtmP2bwr6t6kKDkOqV3q5w8aZcV2lLueoWBX3YlIBF1ZgMZ",
                'to': next_user.tel1,
                'message': f'درخواست شماره {company.woPartWorkorder.id}  با مشخصات زیر نیاز به تایید شما دارد: \n\n {company.getItems3()} \n\n 【سیستم مدیریت نگهداری تعمیرات اکسپرتر】\n\n    ꧁سرو رایان ꧂  \n🌐 https://sarvrayan.ir',
                }
                
                # files=PurchaseRequestFile.objects.filter(file__isnull=False,purchase_request=company)
                files2=[]
                # files=list(files)
                # for i in files:
                #     with i.file.open('rb') as file_obj:

                #         files2.append(file_obj)

                headers = {}
                response = rqt.request("POST", url, headers=headers, data=payload, files=files2)
    return JsonResponse({"status":"ok"})
def wtf_find_users_by_group(group_name):
    """
    Function to find users belonging to a specific group name
    
    Args:
        request: HTTP request object
        group_name: String representing the name of the group
    
    Returns:
        HttpResponse containing list of users or error message
    """
    try:
        # Get the group object based on the name
        group = Group.objects.get(name=group_name)
        
        # Get all users that belong to this group
        users = User.objects.filter(groups=group)
        return users
        
    except ObjectDoesNotExist:
        return 