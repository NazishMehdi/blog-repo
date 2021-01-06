from django import forms
from myapp.models import Comment
class EmailSentForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')