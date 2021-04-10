from django import forms
from .models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('user', 'title', 'body')

        # this is how to create widgets that will correspond to css using class
        # field which will have the field type which will have attributes ie attrs which will have class
        widgets = {
            'title': forms.TextInput(attrs={'class': 'posttitleclass'}),
            'body': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontentclass'}),
        }
        # in body the class postcontentclass is the class we defined or we made
        # editable medium-editor-textarea is a class which we are gonna prob do is pip install it
        # ie it is from external source


class CommentsForm(forms.ModelForm):

    class Meta():
        model = Comments
        fields = ('user', 'body')

        widgets = {
            'user': forms.TextInput(attrs={'class': 'posttitleclass'}),
            'body': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
