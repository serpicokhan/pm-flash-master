from pyfcm import FCMNotification
from cmms.models import SysUser
API_KEY="AIzaSyCXtTSMxPAxR7WsI_m5AAhfJWFdwd9QIxg"
class push_notification:
    @staticmethod
    def send_push(rec_id,title,body):
        push_service = FCMNotification(api_key='AAAAClhesu0:APA91bGeNZ2q5BhmwbpyJ0vjQn87BKDMk62-f2b3zDfB12Xcar73auyyVvkgGvVvThdsUdI8GV_j-qQC7jEPnRrkWwTXknkJyhH_t4sPOm0KYk1RuzkyUALR7FMm2phxQZfuhbo57pco')
        # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

        registration_id = rec_id
        message_title = title
        message_body = body
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return result
    @staticmethod
    def find_user_token(userId):
        return SysUser.objects.get(pk=id).token
