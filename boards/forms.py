from django import forms
from .models import Board

# class BoardForm(forms.Form):
#     title = forms.CharField(label="제목", widget=forms.TextInput(attrs={
#                                                         'placeholder': 'THE TITLE!',
#                                              }))
#     content =  forms.CharField(label="내용", 
#                               error_messages={'required': '내용을 입력해주세요!'},
#                               widget=forms.Textarea(attrs={
#                                                         'class': 'Content-input',
#                                                         'rows': 5,
#                                                         'cols': 50,
#                                                         'placeholder': 'Fill the Content~'
#                                              }))

# 더 짧게!
class BoardForm(forms.ModelForm):
    # Model의 정보를 작성하는 곳
    class Meta:
        model = Board
        # models.py에 지정해놓은 필드를 사용한다.
        fields = '__all__'
        widgets = {'title': forms.TextInput(attrs={
                                                'placeholder':'제목을 입력하세요.',
                                                'class': 'title'}),
                  'content': forms.Textarea(attrs={
                                                'placeholder':'내용을 입력하세요.',
                                                'class': 'content',
                                                'rows': 5,
                                                'cols': 50,})
                }
        error_messages = {
                          'title': {'required': '입력하시라고요.'},
                          'content': {'required': '입력 하.시.라.고.요.'}
                          }
                            