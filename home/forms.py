from django import forms

class NewUserCreationForm(forms.Form):
    username=forms.CharField(label='Username', max_length=100)
    password=forms.CharField(max_length=32,widget=forms.PasswordInput)
    confirmpassword=forms.CharField(max_length=32,widget=forms.PasswordInput)

class AuthenticationForm(forms.Form):
    username=forms.CharField(label='Username', max_length=100)
    password=forms.CharField(max_length=32,widget=forms.PasswordInput)
    

class SearchForm(forms.Form):
    to_search = forms.CharField(label='To-Search', max_length= 100)
