from django.shortcuts import render,redirect
from django.views import View
from .forms import Custom_UserForm,IdentifyUserForm,VerifyOtpForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from coreapp.models import ProductModel,CategoriesModel
# Create your views here.

class RegisterView(View):

    def get(self,request,*args,**kwargs):
        fm=Custom_UserForm()
        context={
            'form':fm,
            'title':'Register'
        }
        return render(request,'authenticate/register.html',context)
    
    def post(self,request,*args,**kwargs):
        fm=Custom_UserForm(data=request.POST)
        if fm.is_valid():
            fname=fm.cleaned_data.get('first_name')
            lname=fm.cleaned_data.get('last_name')
            email=fm.cleaned_data.get('email')
            username=fm.cleaned_data.get('username')
            fm.save()
            msg=f"Hi {fname} {lname} \n welcome to Ecommerce application your account has been Created Succefully with the username: {username}"
            send_mail(
                "Account Registration",
                msg,
                "adarshadi7760@gmail.com",
                [email],
                fail_silently=False
            )

            return redirect('login')
        messages.error(request,f'{fm.errors}')
        return redirect('register')    

class LoginView(View):
    
    def get(self,request,*args,**kwargs):

        context={
            'Loginform':AuthenticationForm(),
            'title':'Log In'
        }

        return render(request,'authenticate/login.html',context)
    
    def post(self,request,*args,**kwargs):
        fm=AuthenticationForm(data=request.POST)

        if fm.is_valid():
            username=fm.cleaned_data.get('username')
            password=fm.cleaned_data.get('password')

            user=authenticate(request,username=username,password=password)

            if user:
                login(request,user)
                return redirect('dashboard')
            
        messages.add_message(request,messages.ERROR,"Invalid Credentials")    
        return redirect('login')
    

class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"User Log out Successfull")
        return redirect('login')

import datetime
from django.utils import timezone
import random

class IdentifyUserSendOtp(View):

    def get(self,request,*args,**kwargs):
        fm=IdentifyUserForm()
        context={
            'form':fm,
            'title':"Identify User"
        }
        return render(request,'authenticate/identifyuser.html',context)

    def post(self,request,*args,**kwargs):
        fm=IdentifyUserForm(request.POST)

        if fm.is_valid():
            usernameoremail=fm.cleaned_data.get('UsernameorEmail')

            user=User.objects.filter(Q(username=usernameoremail) | Q(email=usernameoremail)).first()
            
            if not user:
                messages.error(request,"User does not Exist Enter Valid Username or Email")
                return redirect('identifyusersendotp')
            
            
            otp= ''.join(str(random.randint(0,9)) for _ in range(5))

            request.session['otp']=otp
            request.session['usernameoremail']=usernameoremail

            send_mail(
                "OTP Verification",
                f"Your Otp is {otp}",
                "adarshadi7760@gmail.com",
                [user.email],
                fail_silently=False
            )

            return redirect('verifyotp')
        
        messages.error(request,"invalid username or email check before you enter")
        return redirect('identifyusersendotp')
    

            
class VerifyOtpLoginView(View):

    def get(self,request,*args,**kwargs):
        fm=VerifyOtpForm()
        context={
            'form':fm,
            'title':'Verify Otp',
            'otp_message':'enter otp within 10 min'
        }
        
        return render(request,'authenticate/verifyotp.html',context)

    def post(self,request,*args,**kwargs):
        fm=VerifyOtpForm(request.POST)

        if fm.is_valid():
            entered_otp=fm.cleaned_data.get('Otp')
            session_otp=request.session.get('otp')
            usernameoremail=request.session.get('usernameoremail')
            
            user=User.objects.filter(Q(username=usernameoremail) | Q(email=usernameoremail)).first()
            
            
            if user and entered_otp==session_otp:
                url='/reset_password/'+user.username+'/'
                messages.success(request,"Reset Your Password")
                return redirect(url)
        
        messages.error(request,"Enter Correct Otp")
        return redirect('verifyotp')
        


class ResetPasswordView(View):
    def get(self,request,*args,**kwargs):
        user=User.objects.filter(username=kwargs['username']).first()
        fm=SetPasswordForm(user=user)
        context={
            'form':fm,
            'title':'Reset Password'
        }

        return render(request,'authenticate/resetpassword.html',context)
    
    def post(self,request,*args,**kwargs):
        user=User.objects.filter(username=kwargs['username']).first()
        fm=SetPasswordForm(data=request.POST,user=user)

        if fm.is_valid():
            fm.save()
            send_mail(
                "Password Reset Succesfull",
                f"Your new password is {user.password}",
                "adarshadi7760@gmail.com",
                [user.email],
                fail_silently=False
            )
            messages.success(request,"Password reset succesfull")
            return redirect('login')
        messages.error(request,f"{fm.errors}")
        return redirect('identifyusersendotp')



@method_decorator(login_required,name='dispatch')
class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        
        trending_products=ProductModel.objects.filter(trending_product=True).prefetch_related('variants')

        electronics = CategoriesModel.objects.get(name="Electronics")
        subcategories = CategoriesModel.objects.filter(parent_category=electronics)

        categories=CategoriesModel.objects.filter(parent_category=None)

        best_electronics = ProductModel.objects.filter(
            category_id__in=subcategories,
            best_product=True
        ).prefetch_related('variants') 


        context = {
            'categories': categories,
            'best_electronics':best_electronics,
            'trending_products':trending_products
        }
        return render(request, 'authenticate/dashboard.html', context)

    


    
    

