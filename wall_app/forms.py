from django import forms
from wall_app.models import Comment


class CommentForm(forms.ModelForm):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=None)
    type = forms.CharField(widget=forms.HiddenInput(), initial='main')

    class Meta:
        model = Comment
        fields = ('text', 'parent', 'user')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': ''}),
            'parent': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }

    def save(self, commit=True):
        comment_id = self.cleaned_data['pk']

        if comment_id:
            try:
                obj = Comment.objects.get(id=comment_id)
                obj.text = self.cleaned_data['text']
                self.instance = obj
            except Comment.DoesNotExist:
                pass

        return super(CommentForm, self).save(commit)
