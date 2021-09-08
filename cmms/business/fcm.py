from pyfcm import FCMNotification
from cmms.models import SysUser
API_KEY="AAAAKhEXPZ8:APA91bH-pd-izfaRaBXxs3szl-_z9vA0z8wsdLqhYps175aMIiHquLdxvQ6skfY5XVESFaxGZWL5UsvGS5lpESb05xzw-KhA3Sdos1wD_klNYpm4o3bRuc8_9pYkXRS8YaX1ARpbfz0A"
class push_notification:
    @staticmethod
    def send_push(api_token,rec_id,title,body):
        push_service = FCMNotification(api_key=api_token)
        # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

        registration_id = rec_id
        message_title = title
        message_body = body
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return result
    @staticmethod
    def find_user_token(userId):
        return SysUser.objects.get(pk=id).token
