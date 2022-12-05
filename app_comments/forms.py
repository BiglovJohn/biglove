from django import forms
from .models import Comments


class CommentsForm(forms.ModelForm):
    """Форма модели комментария"""
    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ['publish_at']

    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        """Работа с классами формы комментариев"""
        # self.fields['comment_text'].widget.attrs['id'] = 'user_comment_text'
