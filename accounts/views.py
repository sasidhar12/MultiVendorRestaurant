from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User
from accounts import forms
from django.contrib import messages
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        #print(request.POST)
        form = forms.UserForm(request.POST)

        if form.is_valid():
            # Getting the password to Hash it
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            #saves the password in Hashed format
            user.set_password(password)
            user.save()
            print("Account was created")
            messages.success(request, "Your accounts has been created successfully!")
            #print(messages)
            return redirect('registerUser')
        else:
            print("Form is not valid")
            
            print(form.errors)
    else:
        form = forms.UserForm()
    context = {'form':form}
    return render(request, 'accounts/registerUser.html',context=context)