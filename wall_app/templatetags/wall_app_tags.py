from django import template

register = template.Library()


@register.filter
def can_edit(user, obj):
    user_can_edit = False

    if user.is_superuser or (hasattr(obj, 'user') and obj.user == user):
        user_can_edit = True

    return user_can_edit
