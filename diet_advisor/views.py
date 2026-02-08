from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from diet_advisor.forms import UserProfileForm,food_upload_form

from diet_advisor.models import UserProfile,Foodlog,PremiumOrder

from django.urls import reverse_lazy

from twilio.rest import Client

from django.conf import settings

import google.generativeai as genai

import json

import razorpay

# Create your views here.

class UserprofileCreateView(LoginRequiredMixin, CreateView):

    model = UserProfile

    form_class = UserProfileForm

    template_name = 'createprofile.html'

    success_url = reverse_lazy('home')

    def form_valid(self, form):

        profile = form.save(commit=False)

        profile.user = self.request.user

        # BMI calculation

        height = profile.height / 100  # cm → m

        bmi = profile.weight / (height ** 2)

        # BMR calculation

        if profile.gender == 'male':

            bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age + 5

        else:

            bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age - 161

        # Activity level 

        if bmi < 18.5:

            activity_level = "sedentary"

            factor = 1.2

        elif bmi < 25:

            activity_level = "lightly_active"

            factor = 1.37

        elif bmi < 30:

            activity_level = "moderatively_active"

            factor = 1.55

        else:

            activity_level = "very_active"

            factor = 1.72

        profile.activity_level = activity_level

        #  Calories calculation

        calories_required = bmr * factor

        if profile.goal == "lose_weight":

            target_calories = calories_required - 400

        elif profile.goal == "gain_weight":

            target_calories = calories_required + 400

        else:

            target_calories = calories_required

        profile.bmi = round(bmi, 2)

        profile.bmr = round(bmr, 2)

        profile.calories_needed = round(target_calories, 2)

        profile.save()

        #  WhatsApp message 
        try:
            message_text = (
                f"Hello {profile.user.username},\n"
                f"BMI: {profile.bmi}\n"
                f"BMR: {profile.bmr}\n"
                f"Daily Calories: {profile.calories_needed}"
            )

            client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )

            twilio_message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=message_text,
                to='whatsapp:+919037772004'
            )

            print("Twilio SID:", twilio_message.sid)

        except Exception as e:

            print("Twilio failed:", e)

        return super().form_valid(form)
    

class UserProfileUpdateView(UpdateView):

    model = UserProfile

    form_class = UserProfileForm

    template_name = 'updateprofile.html'   

    success_url = reverse_lazy('home')

    def form_valid(self, form):

        profile = form.save(commit=False)

        # bmi calculation

        height = profile.height / 100

        bmi = profile.weight / (height ** 2)

        # bmr calculations

        if profile.gender == 'male':

            bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age + 5
        else:
            bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age - 161

        # activity level
        
        if bmi < 18.5:

            activity_level = 'sedentary'

            factor = 1.2

        elif bmi < 25:

            activity_level = 'lightly active'

            factor = 1.37

        elif bmi < 30:

            activity_level = 'moderatively active'

            factor = 1.55

        else:

            activity_level = 'very active'

            factor = 1.75

        profile.activity_level = activity_level

        # calories needed

        calories_required = bmr * factor

        if profile.goal == 'lose_weight':

            target_calory = calories_required - 400

        elif profile.goal == 'gain_weight':

            target_calory = calories_required + 400

        else:

            target_calory = calories_required

        profile.bmi = bmi

        profile.bmr = bmr

        profile.calories_needed = target_calory

        profile.save()

        return super().form_valid(form) 

class UserProfileDetailView(View):
    
    def get(self,request):
        
        profile = UserProfile.objects.get(user=request.user)
        
        return render(request,'profile_detail.html',{'profile':profile})
    
class UserProfileResultView(View):
    
    def get(self,request):
        
        profile = UserProfile.objects.get(user=request.user) 
        
        return render(request,'result.html',{'profile':profile})

class UserprofiledeleteView(View):
    def get(self,request,**kwargs):
        id = kwargs.get("pk")
        obj =  get_object_or_404(UserProfile,id=id)
        obj.delete()
        return redirect('home')
    
    # model = UserProfile
    
    # form_class = UserProfileForm
    
    # template_name = 'createprofile.html'
    
    # success_url = reverse_lazy('home')

    def get_queryset(self):
        
        return UserProfile.objects.filter(user=self.request.user)

class FoodLogView(CreateView):

    model = Foodlog

    form_class = food_upload_form

    template_name = "addfood.html"

    def form_valid(self,form):

        food = form.save(commit=False)

        food.user = self.request.user
        
        print(self.request.user)

        food.userprofile = UserProfile.objects.get(user = self.request.user)

        food_image = self.request.FILES.get("food_image")

        genai.configure(api_key = "AIzaSyCvLQlZYSpxCNx8oHVBZfuMgVQcQQtjGpQ" )
        
        image_bytes = food_image.read()

        model = genai.GenerativeModel("gemini-2.5-flash",
                                       generation_config ={
                                           "response_mime_type":"application/json"
                                       })

        prompt = """ 

        identify this food item and return response strictly and only in this json format
        {
        "food_name":"",
        "quantity":"",
        "calories":""
        }

        """
        response = model.generate_content([prompt,{'mime_type':food_image.content_type,'data':image_bytes}])

        result = response.text

        data = json.loads(result)

        food.food_name = data['food_name']

        food.quantity = data['quantity']

        food.calories_detected = data['calories']

        food.save()

        print(data)

        print(food.id)

        return redirect("result",pk = food.id)
    
        print("hello")

    
class FoodresultView(View):

        def get(self,request,**kwargs):

            id = kwargs.get("pk")

            food = Foodlog.objects.get(id = id)

            return render (request,"food_result.html",{"food":food})
        
class CreatePremiumView(View):

    template_name ="premium_payment.html"

    def get(self,request):

        amount =10000

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))

        razorpay_order = client.order.create({
            'amount':amount,
            'currency':'INR'
        })

        order_id = razorpay_order['id']

        order = PremiumOrder.objects.create(user = request.user,
                                            order_id = order_id,
                                            amount = amount)
        
        return render(request,"payment.html",{"order":order,
                                              "amount":amount,
                                              "key_id":settings.RAZOR_KEY_ID})

class PaymentSuccessView(View):

    def post(self,request):

        payment_id = request.POST.get('razorpay_payment_id')

        order_id = request.POST.get('razorpay_order_id')

        signature =  request.POST.get('razorpay_signature')

        order = PremiumOrder.objects.get(order_id = order_id)

        order.payment_id = payment_id

        order.signature = signature

        order.is_paid = True

        order.save()

        return redirect('home')


        







