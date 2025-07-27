# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from cmms.models import Notification
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group

def get_notifications_cmms(request):
    if not request.user.is_authenticated:
        return JsonResponse({'notifications': []})
    def humanize_time_diff(dt):
        now = timezone.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        minutes = int(seconds // 60)
        hours = int(minutes // 60)
        days = int(hours // 24)
        
        if days > 0:
            return f"{days} روز قبل" if days == 1 else f"{days} روز قبل"
        elif hours > 0:
            return f"{hours} ساعت قبل" if hours == 1 else f"{hours} ساعت قبل"
        elif minutes > 0:
            return f"{minutes} دقیقه قبل" if minutes == 1 else f"{minutes} دقیقه قبل"
        else:
            return "همین حالا"
    
    notifications = Notification.objects.filter(user=request.user.sysuser, read=False).order_by('created_at')
    
    data = [{
        'message': n.message,
        'user':n.user,
        'id': n.id,
        'link': n.link,
        'time_ago': humanize_time_diff(n.created_at),
        'created_at': n.created_at.strftime("%Y-%m-%d %H:%M")
    } for n in notifications]
    data2=dict()
    
    data2["html_mail_list"]=render_to_string('cmms/mail/notif.html', {
        'mails': data,
        'count':notifications.count()
    })
    return JsonResponse(data2)

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({'success': True})



def send_message_to_group_x(request,group_name,message,link):
    # Check if the requesting user has permission to send messages
    if not request.user.is_authenticated:
        return False
    
    # You might want to add additional permission checks here
    # if not request.user.has_perm('app_name.can_send_group_messages'):
    #     return HttpResponse("Permission denied", status=403)
    
    # Get the group named 'x' (case-sensitive)
    try:
        group_x = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        print(request, "Group 'x' does not exist")
        return False
    
    # Get all users in group 'x'
    users_in_group_x = group_x.user_set.all()
    
    # Example message content - you might get this from a form
    message_content = "This is an important message for group X members"
    
    # For demonstration, we'll use Django's messaging framework
    # In a real application, you might send emails, notifications, etc.
    for user in users_in_group_x:
        # Here you would implement your actual messaging logic
        # For example, sending an email:
        # send_mail(
        #     'Message for Group X',
        #     message_content,
        #     'from@example.com',
        #     [user.email],
        #     fail_silently=False,
        # )
        notification = Notification.objects.create(
        user=user.sysuser,
        message=message,
        link=link
        )
        
        # For this example, we'll just print to console
        print(f"Message sent to {user.username}: {message_content}")
    
    # Add a success message for the requester
    # messages.success(request, f"Message sent to {users_in_group_x.count()} users in group X")
    
    return True