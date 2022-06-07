from django.template.defaulttags import register
from django import template
from Offers.models import Company
register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def user_has_company(request):
    company = Company.objects.filter(user=request.user.pk)
    if company:
        return True
    else:
        return False