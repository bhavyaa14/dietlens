from django.db import models

from user_app.models import CustomUser

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    age = models.IntegerField()

    gender = models.CharField(max_length=30,choices=[('male','male'),
                                                     ('female','female')])

    height = models.FloatField()

    weight = models.FloatField()

    activity_level =models.CharField(max_length= 30,choices=[('sedentary','sedentary'),
                                                             ('lightly_active','lightly active'),
                                                             ('moderatively_active','moderatively active'),
                                                             ('very_active','very active')])

    goal = models.CharField(max_length= 100, choices=[('lose_weight','lose_weight'),
                                                      ('gain_weight','gain_weight'),
                                                      ('maintain_weight','maintain_weight')])

    bmi = models.FloatField(null = True , blank = True)

    bmr = models.FloatField(null = True , blank = True)
    
    calories_needed = models.FloatField(null = True , blank = True)

class Foodlog(models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    food_name = models.CharField(max_length=100,blank=True,null=True)

    quantity = models.CharField(max_length=100,blank=True,null=True)

    calories_detected = models.CharField(max_length=100)

    food_image = models.ImageField(upload_to="foodimage/")

    created_date = models.DateField(auto_now_add=True)

    calories_status = models.CharField(max_length=100)


class PremiumOrder(models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    order_id = models.CharField(max_length=30)

    amount = models.IntegerField()

    payment_id = models.CharField(max_length=50)

    signature  = models.CharField(max_length=50)

    is_paid = models.BooleanField(default=False)

    created_at =models.DateTimeField(auto_now_add=True)