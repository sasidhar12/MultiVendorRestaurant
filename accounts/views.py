from django.shortcuts import render,redirect
from django.http import HttpResponse
from accounts.utils import detectUser
from .models import User
from accounts import forms
from .models import UserProfile
from django.contrib import messages
from django.contrib import auth
from vendor.forms import VendorForm
from .forms import UserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.


#Restrict the vendor from accessing the customer dashboard 
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        # This error comes from django.core.exceptions
        raise PermissionDenied
#  customer from accessing the vendors
def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied
    


def registerUser(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already an existing user!")
        return redirect('myAccount')
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
            user.is_active=True
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

def redirectAccount(user):
    if user == "Vendor":
        redirectUrl = "vendorDashboard"
        return redirectUrl
    elif user == "Customer":
        redirectUrl = "customerDashboard"
        return redirectUrl
    
    elif user == None and user.is_superadmin:
        redirectUrl = 'admin'
        return redirectUrl
    

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myAccount')
    
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # Returns the user object if the credentials are valid
        user = auth.authenticate(request=request, email=email,password=password)
         
        
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are logged in")
            # # redirect_url = detectUser(user)
            # # print("=======================================================")
            # # print(redirect_url)
            # # print("======================================================")
            # return redirect(redirect_url)
            return redirect('myAccount')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')


@login_required(login_url='login',) 
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')


@user_passes_test(check_role_vendor)
@login_required(login_url='login',)
def venodrDashboard(request):
    return render(request,'accounts/vendorDashboard.html')



@login_required(login_url='login',)
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)
