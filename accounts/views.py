from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User
from accounts import forms
from .models import UserProfile
from django.contrib import messages

from vendor.forms import VendorForm
from .forms import UserForm
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        #print(request.POST)
        form = forms.UserForm(request.POST)

        if form.is_valid():
            # Getting the password to Hash it
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            username=username,
                                            email=email,
                                            password=password)
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


def registerVendor(request):
    if request.method == 'POST':
        #store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES )

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            username=username,
                                            email=email,
                                            password=password)
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been created succcessfully please wait for the approval")
            return redirect('registerVendor')

        else:
            print("Invalid")
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form':form,
        'v_form':v_form
    }
    return render(request,'accounts/registerVendor.html', context=context)


def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return render(request,'You are logged out')

def dashboard(request):
    return render(request,'Dashboard')
