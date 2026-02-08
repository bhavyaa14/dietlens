from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View

from user_app.forms import UserregisterForm,Forgotemailform,Otpverifyform,Resetpasswordform

from user_app.models import CustomUser

from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail

import random

from django.contrib.auth.hashers import make_password

class SignupView(View):

    def get(self,request):

        form = UserregisterForm()

        return render(request,"signup.html",{"form":form})
    
    def post(self,request):

        print(request.POST)

        form = UserregisterForm(request.POST) #form:cleaned_data

        # username = request.POST.get("username")

        # mobile_number = request.POST.get("mobile_number")

        # email = request.POST.get("email")

        # password = request.POST.get("password")

        # CustomUser.objects.create_user(username = username,
        #                                mobile_number = mobile_number,
        #                                email= email,
        #                                password= password)
        
        # return render(request,"signup.html",{"form":form})

        if  form.is_valid():

            print (form.cleaned_data)

            CustomUser.objects.create_user(username = form.cleaned_data.get("username"),
                                           mobile_number = form.cleaned_data.get("mobile_number"),
                                           email = form.cleaned_data.get("email"),
                                           password= form.cleaned_data.get("password") )
            
               
            
            return render(request,"signup.html")
        
        return render(request,"signup.html")
    
class SigninView(View):

    def get(self,request):

        return render(request,"signin.html")
    
    def post(self,request):

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)

        if user:

            login(request,user)

            print("hello")

            return redirect("home")
        
        print("no")

        return render(request,"signin.html")

class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect("signin")
    

class ForgotpasswordView(View):
    
    def get(self,request):
        
        form = Forgotemailform()
        
        return render(request,'forgot.html',{'form':form})
    
    def post(self,request):
        
        email=request.POST.get('email')
        
        user=CustomUser.objects.get(email=email)
        
        if user:
            
            otp_generate = random.randint(1000,9999)
            
            request.session['otp']=otp_generate
            
            request.session['email']=email
            
            send_mail(subject='forgot password',
                      message=str(otp_generate),
                      from_email='bhavyaprabhath14@gmail.com',
                      recipient_list=[email])
            print('done')
            
        # return render(request,'forgot.html')
            return redirect('verify')
        
        form=Forgotemailform()
        
        return render(request,'forgot.html',{'form':form})

class OtpverifyView(View):

    def get(self,request):

        form = Otpverifyform()

        return render(request,"verify.html",{"form":form})
    
    def post(self,request):

        form = Otpverifyform(request.POST)

        otp = request.POST.get("otp")

        if request.session.get('otp') ==int(otp):

            return redirect("reset")

        return render(request,"verify.html",{"form":form})
    
class ResetpasswordView(View):

    def get(self,request):

        form = Resetpasswordform()

        return render(request,"reset.html",{"form":form})
    
    def post(self,request):

        new_password = request.POST.get("new_password")

        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:

            return render(request,"reset.html")
        
        email = request.session.get("email")

        user = CustomUser.objects.get(email = email)

        user.password = make_password(new_password)

        user.save()

        return redirect("signin")
    
class BaseView(View):

    def get (self,request):

        return render(request,"home.html")







    


    

    



    

    



        