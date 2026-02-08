from django import forms

from user_app.models import CustomUser

class UserregisterForm(forms.ModelForm):

    class Meta:

        model = CustomUser

        fields = ["username","mobile_number","email","password"]

        widgets ={
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Your Username"
            }),
            "mobile_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder":"Enter Your Mobile Number"
            }),
            "email": forms.TextInput(attrs={
                 "class":"form-control",
                 "placeholder":"Enter Your Email Address"
             }),
            "password": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter Your Password"
             }),
        }

class Forgotemailform(forms.Form):

    email = forms.CharField(max_length= 30)


class Otpverifyform(forms.Form):

    otp = forms.CharField(max_length=10)

class Resetpasswordform(forms.Form):

    new_password = forms.CharField(max_length= 30)

    confirm_password = forms.CharField(max_length= 30)