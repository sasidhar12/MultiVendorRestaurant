from typing import Any
from django import forms
from . models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User # Module that we want to modify or replicate
        fields = ['first_name','last_name','username','email','password']
    
    def clean(self):
        # Overwrites the clean method
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password Does not match!"
            )
        

        
        # Next step is to go to views and from views call this form class i.e UserForm