from django import forms

from diet_advisor.models import UserProfile,Foodlog

class UserProfileForm(forms.ModelForm):

    class Meta:

        model =UserProfile

        fields = ['age','gender','height','weight','goal']

        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'form-control rounded-3'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control rounded-3'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control rounded-3'
            }),
            'goal': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
        }

class food_upload_form(forms.ModelForm):

    class Meta:

        model = Foodlog

        fields = ["food_image"]  

    