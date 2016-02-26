from django.contrib import admin
from django import forms
from wall_app.models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_except', 'user', 'created_at']
    list_per_page = 25

    """def get_form(self, request, obj=None, **kwargs):
        form = super(CommentAdmin, self).get_form(request, obj, **kwargs)

        qs = Comment.objects.all()

        if obj:
            qs = qs.exclude(id=obj.id)

        choices = list(qs.values_list('id', 'text'))

        choices.insert(0, (0, '---------'))

        form.base_fields['parent'] = forms.ChoiceField(choices=choices, required=False)

        return form"""
