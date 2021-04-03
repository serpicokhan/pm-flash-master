from django import template

register = template.Library()
@register.simple_tag
def get_user(request):
    if(request.user.is_authenticated()):
        return request.user
    else:
        return "no user"
        
