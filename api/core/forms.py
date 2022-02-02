from django import forms


# class FeedBackForm(forms.Form):
#     name = forms.CharField(
#         max_length=100,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'name',
#             'placeholder': "Ваше имя"
#         })
#     )
#     email = forms.CharField(
#         max_length=100,
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'id': 'email',
#             'placeholder': "Ваша почта"
#         })
#     )
#     subject = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'subject',
#             'placeholder': "Тема"
#         })
#     )
#     message = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'class': 'form-control md-textarea',
#             'id': 'message',
#             'rows': 2,
#             'placeholder': "Ваше сообщение"
#         })
#     )